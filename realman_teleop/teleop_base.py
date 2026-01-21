"""
Base Teleoperation Module

Abstract base class for all teleoperation interfaces.
"""

import logging
from abc import ABC, abstractmethod
from typing import Optional
from .robot_controller import RobotController
from .safety import SafetyMonitor

logger = logging.getLogger(__name__)


class TeleopBase(ABC):
    """
    Abstract base class for teleoperation interfaces.
    
    All teleoperation modes (keyboard, joystick, etc.) inherit from this class.
    """
    
    def __init__(
        self,
        robot: RobotController,
        update_rate: float = 100.0,
        enable_safety: bool = True
    ):
        """
        Initialize teleoperation base.
        
        Args:
            robot: RobotController instance
            update_rate: Control loop update rate in Hz
            enable_safety: Whether to enable safety monitoring
        """
        self.robot = robot
        self.update_rate = update_rate
        self.update_period = 1.0 / update_rate
        
        self.running = False
        self.enabled = False  # Deadman switch state
        
        # Safety monitor
        self.safety = None
        if enable_safety:
            self.safety = SafetyMonitor(robot)
        
        logger.info(f"Initialized {self.__class__.__name__} at {update_rate} Hz")
    
    @abstractmethod
    def setup(self) -> bool:
        """
        Setup teleoperation interface.
        
        Returns:
            True if setup successful
        """
        pass
    
    @abstractmethod
    def read_input(self) -> dict:
        """
        Read input from control device.
        
        Returns:
            Dictionary containing input state
        """
        pass
    
    @abstractmethod
    def process_input(self, input_state: dict) -> dict:
        """
        Process raw input into robot commands.
        
        Args:
            input_state: Raw input state from read_input()
            
        Returns:
            Dictionary containing processed commands
        """
        pass
    
    @abstractmethod
    def send_commands(self, commands: dict) -> bool:
        """
        Send commands to robot.
        
        Args:
            commands: Processed commands from process_input()
            
        Returns:
            True if commands sent successfully
        """
        pass
    
    @abstractmethod
    def cleanup(self):
        """Cleanup teleoperation interface."""
        pass
    
    def enable(self):
        """Enable robot control (deadman switch pressed)."""
        if not self.enabled:
            self.enabled = True
            logger.info("Robot control ENABLED")
    
    def disable(self):
        """Disable robot control (deadman switch released)."""
        if self.enabled:
            self.enabled = False
            logger.info("Robot control DISABLED")
            # Stop robot when disabled
            self.robot.stop()
    
    def emergency_stop(self):
        """Trigger emergency stop."""
        logger.critical("EMERGENCY STOP ACTIVATED!")
        self.robot.stop()
        self.disable()
        self.running = False
    
    def run(self):
        """
        Main teleoperation loop.
        
        This is the main control loop that reads input, processes it,
        and sends commands to the robot.
        """
        import time
        
        logger.info("Starting teleoperation...")
        
        if not self.setup():
            logger.error("Setup failed, cannot start teleoperation")
            return
        
        self.running = True
        
        try:
            while self.running:
                loop_start = time.time()
                
                # Read input from device
                input_state = self.read_input()
                
                # Check for emergency stop
                if input_state.get('emergency_stop', False):
                    self.emergency_stop()
                    break
                
                # Check deadman switch
                if input_state.get('enable', False):
                    self.enable()
                else:
                    self.disable()
                
                # Process and send commands only if enabled
                if self.enabled:
                    commands = self.process_input(input_state)
                    
                    # Safety check
                    if self.safety:
                        commands = self.safety.check_commands(commands)
                    
                    self.send_commands(commands)
                
                # Maintain update rate
                loop_time = time.time() - loop_start
                if loop_time < self.update_period:
                    time.sleep(self.update_period - loop_time)
                else:
                    logger.warning(f"Loop time {loop_time:.4f}s exceeds period {self.update_period:.4f}s")
        
        except KeyboardInterrupt:
            logger.info("Teleoperation interrupted by user")
        
        except Exception as e:
            logger.error(f"Error in teleoperation loop: {e}", exc_info=True)
        
        finally:
            self.cleanup()
            logger.info("Teleoperation stopped")
    
    def stop(self):
        """Stop the teleoperation loop."""
        self.running = False
