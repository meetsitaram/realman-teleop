"""
Keyboard Teleoperation Module

Keyboard-based control for RealMan robotic arms.
"""

import logging
import sys
from typing import Dict
import pygame
from .teleop_base import TeleopBase
from .robot_controller import RobotController

logger = logging.getLogger(__name__)


class KeyboardTeleop(TeleopBase):
    """
    Keyboard-based teleoperation for RealMan robots.
    
    Uses pygame for cross-platform keyboard input handling.
    """
    
    # Default key mappings
    DEFAULT_KEY_MAP = {
        # Linear movement (Cartesian space)
        pygame.K_w: 'forward',      # +X
        pygame.K_s: 'backward',     # -X
        pygame.K_a: 'left',         # +Y
        pygame.K_d: 'right',        # -Y
        pygame.K_q: 'up',           # +Z
        pygame.K_e: 'down',         # -Z
        
        # Rotation (Cartesian space)
        pygame.K_i: 'rotate_x_pos',  # +RX
        pygame.K_k: 'rotate_x_neg',  # -RX
        pygame.K_j: 'rotate_y_pos',  # +RY
        pygame.K_l: 'rotate_y_neg',  # -RY
        pygame.K_u: 'rotate_z_pos',  # +RZ
        pygame.K_o: 'rotate_z_neg',  # -RZ
        
        # Control
        pygame.K_SPACE: 'emergency_stop',
        pygame.K_LSHIFT: 'enable',
        pygame.K_RSHIFT: 'enable',
        pygame.K_TAB: 'mode_switch',
        pygame.K_EQUALS: 'speed_up',    # +
        pygame.K_MINUS: 'speed_down',    # -
        
        # Joint control mode (numbers 1-7)
        pygame.K_1: 'joint_1_neg',
        pygame.K_2: 'joint_2_neg',
        pygame.K_3: 'joint_3_neg',
        pygame.K_4: 'joint_4_neg',
        pygame.K_5: 'joint_5_neg',
        pygame.K_6: 'joint_6_neg',
        pygame.K_7: 'joint_7_neg',
        
        # Home position
        pygame.K_h: 'go_home',
    }
    
    def __init__(
        self,
        robot: RobotController,
        update_rate: float = 100.0,
        key_map: Dict[int, str] = None,
        linear_speed: float = 0.1,
        angular_speed: float = 0.3,
        joint_speed: float = 5.0,
    ):
        """
        Initialize keyboard teleoperation.
        
        Args:
            robot: RobotController instance
            update_rate: Control loop rate in Hz
            key_map: Custom key mapping (uses default if None)
            linear_speed: Linear velocity in m/s
            angular_speed: Angular velocity in rad/s
            joint_speed: Joint velocity in deg/s
        """
        super().__init__(robot, update_rate)
        
        self.key_map = key_map or self.DEFAULT_KEY_MAP
        self.linear_speed = linear_speed
        self.angular_speed = angular_speed
        self.joint_speed = joint_speed
        
        self.mode = "cartesian"  # cartesian or joint
        self.current_velocity = [0.0] * 6  # [vx, vy, vz, wx, wy, wz]
        
        self.screen = None
    
    def setup(self) -> bool:
        """Setup pygame and display window."""
        try:
            pygame.init()
            
            # Create a small window for focus
            self.screen = pygame.display.set_mode((640, 480))
            pygame.display.set_caption("RealMan Robot Keyboard Control")
            
            # Fill screen with instructions
            self._display_instructions()
            
            logger.info("Keyboard teleoperation setup complete")
            logger.info(f"Mode: {self.mode}")
            logger.info(f"Linear speed: {self.linear_speed} m/s")
            logger.info(f"Angular speed: {self.angular_speed} rad/s")
            
            return True
            
        except Exception as e:
            logger.error(f"Setup failed: {e}")
            return False
    
    def _display_instructions(self):
        """Display control instructions on pygame window."""
        if not self.screen:
            return
        
        font = pygame.font.Font(None, 24)
        self.screen.fill((0, 0, 0))
        
        instructions = [
            "RealMan Robot Keyboard Control",
            "",
            "Movement (Cartesian):",
            "  W/S: Forward/Backward (X)",
            "  A/D: Left/Right (Y)",
            "  Q/E: Up/Down (Z)",
            "",
            "Rotation:",
            "  I/K: Rotate X",
            "  J/L: Rotate Y",
            "  U/O: Rotate Z",
            "",
            "Control:",
            "  SHIFT: Enable (hold)",
            "  SPACE: Emergency Stop",
            "  TAB: Switch Mode",
            "  +/-: Speed Up/Down",
            "  H: Go Home",
            "",
            f"Current Mode: {self.mode.upper()}",
            f"Status: {'ENABLED' if self.enabled else 'DISABLED'}",
        ]
        
        y = 20
        for line in instructions:
            text = font.render(line, True, (255, 255, 255))
            self.screen.blit(text, (20, y))
            y += 25
        
        pygame.display.flip()
    
    def read_input(self) -> dict:
        """Read keyboard input."""
        input_state = {
            'linear': [0.0, 0.0, 0.0],
            'angular': [0.0, 0.0, 0.0],
            'joint_deltas': [0.0] * self.robot.dof,
            'enable': False,
            'emergency_stop': False,
            'mode_switch': False,
            'speed_change': 0,
            'go_home': False,
        }
        
        # Process pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                input_state['emergency_stop'] = True
        
        # Get current key states
        keys = pygame.key.get_pressed()
        
        # Check each mapped key
        for key_code, action in self.key_map.items():
            if keys[key_code]:
                if action == 'enable':
                    input_state['enable'] = True
                elif action == 'emergency_stop':
                    input_state['emergency_stop'] = True
                elif action == 'mode_switch':
                    if not hasattr(self, '_mode_switch_pressed'):
                        self._mode_switch_pressed = True
                        input_state['mode_switch'] = True
                elif action == 'go_home':
                    input_state['go_home'] = True
                elif action == 'speed_up':
                    input_state['speed_change'] = 1
                elif action == 'speed_down':
                    input_state['speed_change'] = -1
                    
                # Linear motion
                elif action == 'forward':
                    input_state['linear'][0] = self.linear_speed
                elif action == 'backward':
                    input_state['linear'][0] = -self.linear_speed
                elif action == 'left':
                    input_state['linear'][1] = self.linear_speed
                elif action == 'right':
                    input_state['linear'][1] = -self.linear_speed
                elif action == 'up':
                    input_state['linear'][2] = self.linear_speed
                elif action == 'down':
                    input_state['linear'][2] = -self.linear_speed
                    
                # Angular motion
                elif action == 'rotate_x_pos':
                    input_state['angular'][0] = self.angular_speed
                elif action == 'rotate_x_neg':
                    input_state['angular'][0] = -self.angular_speed
                elif action == 'rotate_y_pos':
                    input_state['angular'][1] = self.angular_speed
                elif action == 'rotate_y_neg':
                    input_state['angular'][1] = -self.angular_speed
                elif action == 'rotate_z_pos':
                    input_state['angular'][2] = self.angular_speed
                elif action == 'rotate_z_neg':
                    input_state['angular'][2] = -self.angular_speed
                    
                # Joint motion
                elif action.startswith('joint_'):
                    joint_num = int(action.split('_')[1]) - 1
                    if joint_num < self.robot.dof:
                        input_state['joint_deltas'][joint_num] = -self.joint_speed
        
        # Reset mode switch flag when key released
        if not keys[pygame.K_TAB]:
            self._mode_switch_pressed = False
        
        return input_state
    
    def process_input(self, input_state: dict) -> dict:
        """Process keyboard input into robot commands."""
        commands = {
            'type': self.mode,
            'velocity': [0.0] * 6,
            'stop': False,
            'home': False,
        }
        
        # Handle mode switch
        if input_state['mode_switch']:
            self.mode = "joint" if self.mode == "cartesian" else "cartesian"
            logger.info(f"Switched to {self.mode.upper()} mode")
            self._display_instructions()
        
        # Handle speed change
        if input_state['speed_change'] != 0:
            factor = 1.1 if input_state['speed_change'] > 0 else 0.9
            self.linear_speed *= factor
            self.angular_speed *= factor
            self.joint_speed *= factor
            logger.info(f"Speed adjusted: linear={self.linear_speed:.3f}, "
                       f"angular={self.angular_speed:.3f}, joint={self.joint_speed:.3f}")
        
        # Handle home command
        if input_state['go_home']:
            commands['home'] = True
            return commands
        
        # Build velocity command based on mode
        if self.mode == "cartesian":
            commands['velocity'] = (
                input_state['linear'] + input_state['angular']
            )
        else:  # joint mode
            commands['velocity'] = input_state['joint_deltas']
        
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
                # For simplicity, we'll use small incremental movements
                # In a real implementation, you'd use velocity control or
                # continuous position updates
                
                if commands['type'] == "cartesian":
                    # Get current pose and apply velocity increment
                    current_pose = self.robot.get_current_pose()
                    if current_pose:
                        # Apply velocity for one time step
                        dt = self.update_period
                        target_pose = [
                            current_pose[i] + commands['velocity'][i] * dt
                            for i in range(6)
                        ]
                        self.robot.movel(target_pose, velocity=50, block=False)
                
                else:  # joint mode
                    # Get current angles and apply delta
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
        """Cleanup pygame resources."""
        if self.screen:
            pygame.quit()
            logger.info("Pygame cleaned up")
