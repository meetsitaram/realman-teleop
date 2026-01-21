"""
Joystick Teleoperation Module

Gamepad/joystick-based control for RealMan robotic arms.
"""

import logging
from typing import Dict, Optional
import pygame
from .teleop_base import TeleopBase
from .robot_controller import RobotController

logger = logging.getLogger(__name__)


class JoystickTeleop(TeleopBase):
    """
    Joystick/gamepad-based teleoperation for RealMan robots.
    
    Supports Xbox, PlayStation, and generic USB controllers.
    """
    
    # Default axis mapping (Xbox controller layout)
    DEFAULT_AXIS_MAP = {
        'linear_x': 1,      # Left stick vertical
        'linear_y': 0,      # Left stick horizontal
        'linear_z': 4,      # Right stick vertical (triggers on some controllers)
        'angular_x': 3,     # Right stick horizontal
        'angular_y': 5,     # Right trigger
        'angular_z': 2,     # Left trigger / D-pad
    }
    
    # Default button mapping (Xbox controller layout)
    DEFAULT_BUTTON_MAP = {
        'enable': 4,             # LB (L1)
        'turbo': 5,              # RB (R1)
        'emergency_stop': 6,     # Back/Select
        'mode_switch': 7,        # Start
        'home': 1,               # B button
    }
    
    def __init__(
        self,
        robot: RobotController,
        update_rate: float = 100.0,
        device_index: int = 0,
        axis_map: Dict[str, int] = None,
        button_map: Dict[str, int] = None,
        deadzone: float = 0.1,
        normal_speed: float = 0.1,
        turbo_speed: float = 0.3,
    ):
        """
        Initialize joystick teleoperation.
        
        Args:
            robot: RobotController instance
            update_rate: Control loop rate in Hz
            device_index: Joystick device index
            axis_map: Custom axis mapping
            button_map: Custom button mapping
            deadzone: Joystick deadzone (0-1)
            normal_speed: Normal speed multiplier
            turbo_speed: Turbo speed multiplier
        """
        super().__init__(robot, update_rate)
        
        self.device_index = device_index
        self.axis_map = axis_map or self.DEFAULT_AXIS_MAP
        self.button_map = button_map or self.DEFAULT_BUTTON_MAP
        self.deadzone = deadzone
        self.normal_speed = normal_speed
        self.turbo_speed = turbo_speed
        
        self.joystick = None
        self.mode = "cartesian"
        self.turbo_active = False
    
    def setup(self) -> bool:
        """Setup pygame and joystick."""
        try:
            pygame.init()
            pygame.joystick.init()
            
            # Check for joysticks
            joystick_count = pygame.joystick.get_count()
            if joystick_count == 0:
                logger.error("No joysticks found!")
                return False
            
            if self.device_index >= joystick_count:
                logger.error(f"Joystick index {self.device_index} not found. "
                           f"Available: 0-{joystick_count-1}")
                return False
            
            # Initialize joystick
            self.joystick = pygame.joystick.Joystick(self.device_index)
            self.joystick.init()
            
            logger.info(f"Joystick connected: {self.joystick.get_name()}")
            logger.info(f"Axes: {self.joystick.get_numaxes()}, "
                       f"Buttons: {self.joystick.get_numbuttons()}")
            logger.info(f"Deadzone: {self.deadzone}")
            logger.info(f"Normal speed: {self.normal_speed}, Turbo: {self.turbo_speed}")
            
            return True
            
        except Exception as e:
            logger.error(f"Setup failed: {e}")
            return False
    
    def read_input(self) -> dict:
        """Read joystick input."""
        input_state = {
            'linear': [0.0, 0.0, 0.0],
            'angular': [0.0, 0.0, 0.0],
            'enable': False,
            'turbo': False,
            'emergency_stop': False,
            'mode_switch': False,
            'home': False,
            'gripper_open': False,
            'gripper_close': False,
            'gripper_half': False,
        }
        
        if not self.joystick:
            return input_state
        
        # Process pygame events
        pygame.event.pump()
        
        # Read axes
        def read_axis(axis_index: int) -> float:
            """Read axis value with deadzone."""
            if axis_index >= self.joystick.get_numaxes():
                return 0.0
            value = self.joystick.get_axis(axis_index)
            return value if abs(value) > self.deadzone else 0.0
        
        # Map axes to linear/angular velocities
        input_state['linear'][0] = read_axis(self.axis_map['linear_x'])
        input_state['linear'][1] = read_axis(self.axis_map['linear_y'])
        input_state['linear'][2] = read_axis(self.axis_map['linear_z'])
        
        input_state['angular'][0] = read_axis(self.axis_map['angular_x'])
        input_state['angular'][1] = read_axis(self.axis_map['angular_y'])
        input_state['angular'][2] = read_axis(self.axis_map['angular_z'])
        
        # Read buttons
        for action, button_index in self.button_map.items():
            if button_index < self.joystick.get_numbuttons():
                if self.joystick.get_button(button_index):
                    input_state[action] = True
        
        return input_state
    
    def process_input(self, input_state: dict) -> dict:
        """Process joystick input into robot commands."""
        commands = {
            'type': self.mode,
            'velocity': [0.0] * 6,
            'stop': False,
            'home': False,
        }
        
        # Handle mode switch
        if input_state['mode_switch']:
            if not hasattr(self, '_mode_switch_pressed'):
                self._mode_switch_pressed = True
                self.mode = "joint" if self.mode == "cartesian" else "cartesian"
                logger.info(f"Switched to {self.mode.upper()} mode")
        else:
            self._mode_switch_pressed = False
        
        # Handle turbo
        self.turbo_active = input_state['turbo']
        speed_multiplier = self.turbo_speed if self.turbo_active else self.normal_speed
        
        # Handle home command
        if input_state['home']:
            commands['home'] = True
            return commands
        
        # Handle gripper controls
        if input_state['gripper_open']:
            if not hasattr(self, '_gripper_open_pressed'):
                self._gripper_open_pressed = True
                self.robot.gripper_open(speed=500, block=False)
                logger.info("Opening gripper")
        else:
            self._gripper_open_pressed = False
        
        if input_state['gripper_close']:
            if not hasattr(self, '_gripper_close_pressed'):
                self._gripper_close_pressed = True
                self.robot.gripper_close(speed=500, force=300, block=False)
                logger.info("Closing gripper")
        else:
            self._gripper_close_pressed = False
        
        if input_state['gripper_half']:
            if not hasattr(self, '_gripper_half_pressed'):
                self._gripper_half_pressed = True
                self.robot.gripper_set_position(500, block=False)
                logger.info("Half-opening gripper")
        else:
            self._gripper_half_pressed = False
        
        # Build velocity command
        commands['velocity'] = [
            input_state['linear'][0] * speed_multiplier,
            input_state['linear'][1] * speed_multiplier,
            input_state['linear'][2] * speed_multiplier,
            input_state['angular'][0] * speed_multiplier,
            input_state['angular'][1] * speed_multiplier,
            input_state['angular'][2] * speed_multiplier,
        ]
        
        return commands
    
    def send_commands(self, commands: dict) -> bool:
        """Send commands to robot."""
        try:
            if commands['home']:
                self.robot.move_to_home()
                return True
            
            if commands['stop']:
                self.robot.stop()
                return True
            
            # Check if there's any movement
            if any(v != 0 for v in commands['velocity']):
                if commands['type'] == "cartesian":
                    current_pose = self.robot.get_current_pose()
                    if current_pose:
                        dt = self.update_period
                        target_pose = [
                            current_pose[i] + commands['velocity'][i] * dt
                            for i in range(6)
                        ]
                        self.robot.movel(target_pose, velocity=50, block=False)
                else:
                    current_joints = self.robot.get_current_joint_angles()
                    if current_joints:
                        dt = self.update_period
                        target_joints = [
                            current_joints[i] + commands['velocity'][i] * dt
                            for i in range(len(current_joints))
                        ]
                        self.robot.movej(target_joints, velocity=50, block=False)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to send commands: {e}")
            return False
    
    def cleanup(self):
        """Cleanup joystick resources."""
        if self.joystick:
            self.joystick.quit()
        pygame.quit()
        logger.info("Joystick cleaned up")


def list_joysticks():
    """List all available joysticks."""
    pygame.init()
    pygame.joystick.init()
    
    count = pygame.joystick.get_count()
    print(f"\nFound {count} joystick(s):")
    
    for i in range(count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        print(f"\nJoystick {i}:")
        print(f"  Name: {joystick.get_name()}")
        print(f"  Axes: {joystick.get_numaxes()}")
        print(f"  Buttons: {joystick.get_numbuttons()}")
        print(f"  Hats: {joystick.get_numhats()}")
        joystick.quit()
    
    pygame.quit()
