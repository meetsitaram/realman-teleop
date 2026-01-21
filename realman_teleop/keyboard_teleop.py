"""
Keyboard Teleoperation Module

Keyboard-based control for RealMan robotic arms.
Automatically detects if running over SSH and uses appropriate input method.
"""

import logging
import sys
import os
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# Try to import pygame, but don't fail if not available
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    logger.warning("Pygame not available, will use terminal mode only")

# Terminal input modules (for SSH mode)
try:
    import select
    import termios
    import tty
    TERMINAL_MODE_AVAILABLE = True
except ImportError:
    TERMINAL_MODE_AVAILABLE = False
    logger.warning("Terminal mode not available (Windows?)")

from .teleop_base import TeleopBase
from .robot_controller import RobotController


def _detect_display():
    """Detect if a display is available."""
    if not PYGAME_AVAILABLE:
        return False
    
    # Check if DISPLAY is set (Linux/Mac)
    if os.environ.get('DISPLAY'):
        return True
    
    # Check if running on Windows (usually has display)
    if sys.platform == 'win32':
        return True
    
    # Check if SSH session
    if os.environ.get('SSH_CONNECTION') or os.environ.get('SSH_CLIENT'):
        return False
    
    # Try to initialize pygame to see if display works
    try:
        pygame.init()
        pygame.display.set_mode((1, 1))
        pygame.quit()
        return True
    except:
        return False


class KeyboardTeleop(TeleopBase):
    """
    Keyboard-based teleoperation for RealMan robots.
    
    Automatically detects environment and uses:
    - Pygame mode (when display available)
    - Terminal mode (when over SSH or no display)
    """
    
    # Terminal key mappings (simple characters)
    TERMINAL_KEY_MAP = {
        'w': 'forward', 's': 'backward',
        'a': 'left', 'd': 'right',
        'q': 'up', 'e': 'down',
        'i': 'rotate_x_pos', 'k': 'rotate_x_neg',
        'j': 'rotate_y_pos', 'l': 'rotate_y_neg',
        'u': 'rotate_z_pos', 'o': 'rotate_z_neg',
        ' ': 'toggle_enable',
        'h': 'go_home',
        'g': 'gripper_open',
        'f': 'gripper_close',
        'v': 'gripper_half',
        '+': 'speed_up', '=': 'speed_up',
        '-': 'speed_down', '_': 'speed_down',
        'x': 'exit',
        '\x1b': 'exit',  # ESC
    }
    
    # Pygame key mappings (when available)
    if PYGAME_AVAILABLE:
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
            
            # Gripper control
            pygame.K_g: 'gripper_open',
            pygame.K_f: 'gripper_close',
            pygame.K_v: 'gripper_half',
        }
    else:
        DEFAULT_KEY_MAP = {}
    
    def __init__(
        self,
        robot: RobotController,
        update_rate: float = 100.0,
        key_map: Optional[Dict] = None,
        linear_speed: float = 0.1,
        angular_speed: float = 0.3,
        joint_speed: float = 5.0,
        force_terminal_mode: bool = False,
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
            force_terminal_mode: Force terminal mode even if display available
        """
        super().__init__(robot, update_rate)
        
        # Detect mode
        self.has_display = _detect_display() and not force_terminal_mode
        self.terminal_mode = not self.has_display
        
        if self.terminal_mode:
            logger.info("Using TERMINAL mode (SSH-compatible)")
            self.key_map = self.TERMINAL_KEY_MAP
            self.toggle_enable = False  # For terminal mode toggle
            # Reduce update rate for terminal mode to accommodate 50ms key timeout
            if update_rate > 15:
                self.update_rate = 15.0
                self.update_period = 1.0 / 15.0
                logger.info(f"Terminal mode: reduced update rate to {self.update_rate} Hz for reliable key detection")
        else:
            logger.info("Using PYGAME mode (Display available)")
            self.key_map = key_map or self.DEFAULT_KEY_MAP
        
        self.linear_speed = linear_speed
        self.angular_speed = angular_speed
        self.joint_speed = joint_speed
        
        self.mode = "cartesian"  # cartesian or joint
        self.current_velocity = [0.0] * 6  # [vx, vy, vz, wx, wy, wz]
        
        self.screen = None
    
    def setup(self) -> bool:
        """Setup input method (pygame or terminal)."""
        try:
            if self.terminal_mode:
                # Terminal mode setup
                self._print_terminal_instructions()
                logger.info("Terminal keyboard teleoperation setup complete")
            else:
                # Pygame mode setup
                pygame.init()
                self.screen = pygame.display.set_mode((640, 480))
                pygame.display.set_caption("RealMan Robot Keyboard Control")
                self._display_instructions()
                logger.info("Pygame keyboard teleoperation setup complete")
            
            logger.info(f"Mode: {self.mode}")
            logger.info(f"Linear speed: {self.linear_speed} m/s")
            logger.info(f"Angular speed: {self.angular_speed} rad/s")
            
            return True
            
        except Exception as e:
            logger.error(f"Setup failed: {e}")
            return False
    
    def _print_terminal_instructions(self):
        """Print instructions for terminal mode."""
        print("\n" + "=" * 70)
        print("KEYBOARD TELEOPERATION (Terminal Mode - SSH Compatible)")
        print("=" * 70)
        print("\n📋 Controls:")
        print("  Enable/Disable:")
        print("    SPACE - Toggle enable/disable (SAFETY SWITCH)")
        print("\n  Movement (when enabled):")
        print("    w/s - Forward/Backward")
        print("    a/d - Left/Right")
        print("    q/e - Up/Down")
        print("\n  Rotation (when enabled):")
        print("    i/k - Pitch up/down")
        print("    j/l - Roll left/right")
        print("    u/o - Yaw left/right")
        print("\n  Gripper:")
        print("    g - Open gripper")
        print("    f - Close gripper")
        print("    v - Half open gripper")
        print("\n  Other:")
        print("    h - Move to home position")
        print("    + - Increase speed")
        print("    - - Decrease speed")
        print("    ESC or x - Exit")
        print("\n" + "=" * 70)
        print("⚠️  WARNING: Robot will move when ENABLED!")
        print("=" * 70)
        print(f"\nCurrent speed: {self.linear_speed:.3f} m/s")
        print("Status: ❌ DISABLED - Press SPACE to enable\n")
    
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
    
    def _get_terminal_key(self):
        """Get a single keypress from terminal (non-blocking)."""
        if not TERMINAL_MODE_AVAILABLE:
            return None
        
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            # Use 50ms timeout - same as working simple script for reliable key detection
            rlist, _, _ = select.select([sys.stdin], [], [], 0.05)
            if rlist:
                ch = sys.stdin.read(1)
                return ch
            return None
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    def _terminal_direct_move(self, key: str, direction: str):
        """Direct movement command for terminal mode (faster, bypasses normal loop)."""
        # Get current pose and apply small increment
        current_pose = self.robot.get_current_pose()
        if not current_pose:
            print(f"\r⚠️  Cannot read pose    ", end='', flush=True)
            return
        
        target_pose = current_pose.copy()
        increment = 0.01  # 1cm or 0.01 rad per keypress
        
        # Apply movement
        if direction == 'X+':
            target_pose[0] += increment
            print(f"\r⬆️  Forward (+X)      ", end='', flush=True)
        elif direction == 'X-':
            target_pose[0] -= increment
            print(f"\r⬇️  Backward (-X)     ", end='', flush=True)
        elif direction == 'Y+':
            target_pose[1] += increment
            print(f"\r⬅️  Left (+Y)         ", end='', flush=True)
        elif direction == 'Y-':
            target_pose[1] -= increment
            print(f"\r➡️  Right (-Y)        ", end='', flush=True)
        elif direction == 'Z+':
            target_pose[2] += increment
            print(f"\r⬆️  Up (+Z)           ", end='', flush=True)
        elif direction == 'Z-':
            target_pose[2] -= increment
            print(f"\r⬇️  Down (-Z)         ", end='', flush=True)
        elif direction == 'RX+':
            target_pose[3] += increment * 0.5
            print(f"\r🔄 Pitch+           ", end='', flush=True)
        elif direction == 'RX-':
            target_pose[3] -= increment * 0.5
            print(f"\r🔄 Pitch-           ", end='', flush=True)
        elif direction == 'RY+':
            target_pose[4] += increment * 0.5
            print(f"\r🔄 Roll+            ", end='', flush=True)
        elif direction == 'RY-':
            target_pose[4] -= increment * 0.5
            print(f"\r🔄 Roll-            ", end='', flush=True)
        elif direction == 'RZ+':
            target_pose[5] += increment * 0.5
            print(f"\r🔄 Yaw+             ", end='', flush=True)
        elif direction == 'RZ-':
            target_pose[5] -= increment * 0.5
            print(f"\r🔄 Yaw-             ", end='', flush=True)
        
        # Send command directly (non-blocking)
        self.robot.movel(target_pose, velocity=30, block=False)
    
    def read_input(self) -> dict:
        """Read keyboard input (terminal or pygame mode)."""
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
        
        if self.terminal_mode:
            # Terminal mode input
            return self._read_terminal_input(input_state)
        else:
            # Pygame mode input
            return self._read_pygame_input(input_state)
    
    def _read_terminal_input(self, input_state: dict) -> dict:
        """Read input in terminal mode."""
        key = self._get_terminal_key()
        
        if key is None:
            input_state['enable'] = self.toggle_enable
            return input_state
        
        # Debug: show what key was pressed (for troubleshooting)
        # print(f"\nDEBUG: Key pressed = {repr(key)}", flush=True)
        
        # Check for exit
        if key in ['x', '\x1b']:  # x or ESC
            input_state['emergency_stop'] = True
            return input_state
        
        # Check for toggle enable (space bar)
        if key == ' ':
            self.toggle_enable = not self.toggle_enable
            if self.toggle_enable:
                print("\r✅ ENABLED - Robot will move!                    ", end='', flush=True)
            else:
                print("\r❌ DISABLED - Press SPACE to enable              ", end='', flush=True)
            input_state['enable'] = self.toggle_enable
            return input_state
        
        # Speed adjustment
        if key in ['+', '=']:
            self.linear_speed = min(self.linear_speed + 0.01, 0.5)
            self.angular_speed = self.linear_speed * 3.0
            status = "ENABLED" if self.toggle_enable else "DISABLED"
            print(f"\r[{status}] Speed: {self.linear_speed:.3f} m/s    ", end='', flush=True)
        elif key in ['-', '_']:
            self.linear_speed = max(self.linear_speed - 0.01, 0.01)
            self.angular_speed = self.linear_speed * 3.0
            status = "ENABLED" if self.toggle_enable else "DISABLED"
            print(f"\r[{status}] Speed: {self.linear_speed:.3f} m/s    ", end='', flush=True)
        elif key == 'h':
            input_state['go_home'] = True
            print("\r🏠 Moving to home position...        ", end='', flush=True)
        elif key == 'g':
            print("\r✋ Opening gripper...                 ", end='', flush=True)
            self.robot.gripper_open(speed=500, block=False)
        elif key == 'f':
            print("\r✊ Closing gripper...                 ", end='', flush=True)
            self.robot.gripper_close(speed=500, force=300, block=False)
        elif key == 'v':
            print("\r🤏 Half-opening gripper...            ", end='', flush=True)
            self.robot.gripper_set_position(500, block=False)
        
        # Set enable state
        input_state['enable'] = self.toggle_enable
        
        # Movement/rotation (only if enabled)
        if self.toggle_enable:
            action = self.key_map.get(key)
            
            # Direct incremental movement for faster response
            if action == 'forward':
                # Send direct movement command for instant response
                self._terminal_direct_move(key, 'X+')
            elif action == 'backward':
                self._terminal_direct_move(key, 'X-')
            elif action == 'left':
                self._terminal_direct_move(key, 'Y+')
            elif action == 'right':
                self._terminal_direct_move(key, 'Y-')
            elif action == 'up':
                self._terminal_direct_move(key, 'Z+')
            elif action == 'down':
                self._terminal_direct_move(key, 'Z-')
            elif action == 'rotate_x_pos':
                self._terminal_direct_move(key, 'RX+')
            elif action == 'rotate_x_neg':
                self._terminal_direct_move(key, 'RX-')
            elif action == 'rotate_y_pos':
                self._terminal_direct_move(key, 'RY+')
            elif action == 'rotate_y_neg':
                self._terminal_direct_move(key, 'RY-')
            elif action == 'rotate_z_pos':
                self._terminal_direct_move(key, 'RZ+')
            elif action == 'rotate_z_neg':
                self._terminal_direct_move(key, 'RZ-')
            else:
                # For non-movement keys, use normal processing
                if action == 'forward':
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
        else:
            if key in 'wsadqeijkluo':
                print("\r⚠️  DISABLED - Press SPACE to enable    ", end='', flush=True)
        
        return input_state
    
    def _read_pygame_input(self, input_state: dict) -> dict:
        """Read input in pygame mode."""
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
                elif action == 'gripper_open':
                    if not hasattr(self, '_gripper_open_pressed'):
                        self._gripper_open_pressed = True
                        self.robot.gripper_open(speed=500, block=False)
                        self.logger.info("Opening gripper")
                elif action == 'gripper_close':
                    if not hasattr(self, '_gripper_close_pressed'):
                        self._gripper_close_pressed = True
                        self.robot.gripper_close(speed=500, force=300, block=False)
                        self.logger.info("Closing gripper")
                elif action == 'gripper_half':
                    if not hasattr(self, '_gripper_half_pressed'):
                        self._gripper_half_pressed = True
                        self.robot.gripper_set_position(500, block=False)
                        self.logger.info("Half-opening gripper")
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
        
        # Reset gripper button flags when keys released
        if not keys[pygame.K_g]:
            self._gripper_open_pressed = False
        if not keys[pygame.K_f]:
            self._gripper_close_pressed = False
        if not keys[pygame.K_v]:
            self._gripper_half_pressed = False
        
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
        """Cleanup resources (pygame or terminal)."""
        if self.terminal_mode:
            print("\n\n")  # Clean up terminal output
            logger.info("Terminal mode cleaned up")
        elif self.screen:
            pygame.quit()
            logger.info("Pygame cleaned up")
