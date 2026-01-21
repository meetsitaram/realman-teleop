#!/usr/bin/env python3
"""
Simple Terminal-Based Keyboard Teleoperation

This is the WORKING version that was fast and responsive.
Keeping it here for reference/comparison.
"""

import sys
import argparse
import logging
import select
import termios
import tty
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from realman_teleop import RobotController
from realman_teleop.config_loader import ConfigLoader
from realman_teleop.utils import setup_logging


class SimpleKeyboardControl:
    """Simple keyboard control using terminal input."""
    
    def __init__(self, robot: RobotController, speed: float = 0.05):
        self.robot = robot
        self.speed = speed
        self.angular_speed = speed * 3.0
        self.enabled = False
        self.running = True
        
    def get_key(self):
        """Get a single keypress from terminal."""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            # Non-blocking read with timeout
            rlist, _, _ = select.select([sys.stdin], [], [], 0.05)
            if rlist:
                ch = sys.stdin.read(1)
                return ch
            return None
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    def print_instructions(self):
        """Print control instructions."""
        print("\n" + "=" * 70)
        print("SIMPLE KEYBOARD TELEOPERATION (Terminal Mode)")
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
        print("\n  Other:")
        print("    h - Move to home position")
        print("    + - Increase speed")
        print("    - - Decrease speed")
        print("    ESC or x - Exit")
        print("\n" + "=" * 70)
        print("⚠️  WARNING: Robot will move when ENABLED!")
        print("=" * 70)
        print(f"\nCurrent speed: {self.speed:.3f} m/s")
        print("Status: ❌ DISABLED - Press SPACE to enable\n")
    
    def run(self):
        """Main control loop."""
        self.print_instructions()
        
        try:
            while self.running:
                key = self.get_key()
                
                if key is None:
                    continue
                
                # Exit
                if key == 'x' or key == '\x1b':  # x or ESC
                    print("\n\n🛑 Exiting...")
                    break
                
                # Speed adjustment
                elif key == '+' or key == '=':
                    self.speed = min(self.speed + 0.01, 0.5)
                    self.angular_speed = self.speed * 3.0
                    status = "ENABLED" if self.enabled else "DISABLED"
                    print(f"\r[{status}] Speed: {self.speed:.3f} m/s    ", end='', flush=True)
                    continue
                elif key == '-' or key == '_':
                    self.speed = max(self.speed - 0.01, 0.01)
                    self.angular_speed = self.speed * 3.0
                    status = "ENABLED" if self.enabled else "DISABLED"
                    print(f"\r[{status}] Speed: {self.speed:.3f} m/s    ", end='', flush=True)
                    continue
                
                # Home position
                elif key == 'h':
                    print("\r🏠 Moving to home position...        ", end='', flush=True)
                    self.robot.move_to_home(velocity=20)
                    status = "ENABLED" if self.enabled else "DISABLED"
                    print(f"\r[{status}] ✓ Home position reached   ", end='', flush=True)
                    continue
                
                # Deadman switch (SPACE toggles enable/disable)
                elif key == ' ':
                    self.enabled = not self.enabled
                    if self.enabled:
                        print("\r✅ ENABLED - Robot will move!         ", end='', flush=True)
                    else:
                        print("\r❌ DISABLED - Press SPACE to enable   ", end='', flush=True)
                    continue
                
                # Movement commands (only if enabled)
                if self.enabled:
                    current_pose = self.robot.get_current_pose()
                    if not current_pose:
                        print("\r⚠️  Cannot read robot pose           ", end='', flush=True)
                        continue
                    
                    target_pose = current_pose.copy()
                    moved = False
                    
                    # Linear movement
                    if key == 'w':
                        target_pose[0] += self.speed * 0.1
                        moved = True
                        print(f"\r⬆️  Forward (+X: {self.speed:.3f})      ", end='', flush=True)
                    elif key == 's':
                        target_pose[0] -= self.speed * 0.1
                        moved = True
                        print(f"\r⬇️  Backward (-X: {self.speed:.3f})     ", end='', flush=True)
                    elif key == 'a':
                        target_pose[1] += self.speed * 0.1
                        moved = True
                        print(f"\r⬅️  Left (+Y: {self.speed:.3f})         ", end='', flush=True)
                    elif key == 'd':
                        target_pose[1] -= self.speed * 0.1
                        moved = True
                        print(f"\r➡️  Right (-Y: {self.speed:.3f})        ", end='', flush=True)
                    elif key == 'q':
                        target_pose[2] += self.speed * 0.1
                        moved = True
                        print(f"\r⬆️  Up (+Z: {self.speed:.3f})           ", end='', flush=True)
                    elif key == 'e':
                        target_pose[2] -= self.speed * 0.1
                        moved = True
                        print(f"\r⬇️  Down (-Z: {self.speed:.3f})         ", end='', flush=True)
                    
                    # Rotation
                    elif key == 'i':
                        target_pose[3] += self.angular_speed * 0.1
                        moved = True
                        print(f"\r🔄 Pitch+ ({self.angular_speed:.3f})  ", end='', flush=True)
                    elif key == 'k':
                        target_pose[3] -= self.angular_speed * 0.1
                        moved = True
                        print(f"\r🔄 Pitch- ({self.angular_speed:.3f})  ", end='', flush=True)
                    elif key == 'j':
                        target_pose[4] += self.angular_speed * 0.1
                        moved = True
                        print(f"\r🔄 Roll+ ({self.angular_speed:.3f})   ", end='', flush=True)
                    elif key == 'l':
                        target_pose[4] -= self.angular_speed * 0.1
                        moved = True
                        print(f"\r🔄 Roll- ({self.angular_speed:.3f})   ", end='', flush=True)
                    elif key == 'u':
                        target_pose[5] += self.angular_speed * 0.1
                        moved = True
                        print(f"\r🔄 Yaw+ ({self.angular_speed:.3f})    ", end='', flush=True)
                    elif key == 'o':
                        target_pose[5] -= self.angular_speed * 0.1
                        moved = True
                        print(f"\r🔄 Yaw- ({self.angular_speed:.3f})    ", end='', flush=True)
                    
                    if moved:
                        self.robot.movel(target_pose, velocity=30, block=False)
                else:
                    if key in 'wsadqeijkluo':
                        print("\r⚠️  DISABLED - Press SPACE to enable    ", end='', flush=True)
        
        except KeyboardInterrupt:
            print("\n\n🛑 Interrupted by user")
        except Exception as e:
            print(f"\n\n❌ Error: {e}")
            logging.exception("Control loop error")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Simple Terminal-Based Keyboard Teleoperation (Works over SSH!)"
    )
    parser.add_argument(
        '--speed',
        type=float,
        default=0.05,
        help='Movement speed in m/s (default: 0.05)'
    )
    parser.add_argument(
        '--log-level',
        type=str,
        default='WARNING',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help='Logging level'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    
    # Load configuration
    config = ConfigLoader.load_env_config()
    robot_config = config.get('robot', {})
    
    print("=" * 70)
    print("Simple Terminal Keyboard Teleoperation (BACKUP VERSION)")
    print("=" * 70)
    print(f"Robot IP: {robot_config.get('ip', '192.168.10.18')}")
    print(f"Robot Model: {robot_config.get('model', 'R1D2')}")
    print("=" * 70)
    
    # Create robot controller
    robot = RobotController(
        ip=robot_config.get('ip', '192.168.10.18'),
        port=robot_config.get('port', 8080),
        model=robot_config.get('model', 'R1D2'),
        dof=robot_config.get('dof')
    )
    
    # Connect to robot
    print("\n🔌 Connecting to robot...")
    if not robot.connect():
        print("❌ Failed to connect to robot. Exiting.")
        return 1
    print("✅ Connected successfully!")
    
    try:
        # Create and run keyboard control
        control = SimpleKeyboardControl(robot, speed=args.speed)
        control.run()
        
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        return 1
    
    finally:
        # Disconnect from robot
        print("\n\n🔌 Disconnecting...")
        robot.disconnect()
        print("✅ Disconnected. Goodbye!")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

