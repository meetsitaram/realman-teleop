#!/usr/bin/env python3
"""
Keyboard Teleoperation Example

Basic example of controlling RealMan robot with keyboard.
"""

import sys
import argparse
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from realman_teleop import RobotController, KeyboardTeleop
from realman_teleop.config_loader import ConfigLoader
from realman_teleop.utils import setup_logging


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="RealMan Robot Keyboard Teleoperation")
    parser.add_argument(
        '--config',
        type=str,
        default='config/robot_config.yaml',
        help='Path to robot configuration file'
    )
    parser.add_argument(
        '--ip',
        type=str,
        help='Robot IP address (overrides config)'
    )
    parser.add_argument(
        '--model',
        type=str,
        choices=['RM65', 'RM75', 'RML63', 'ECO65', 'GEN72', 'R1D2'],
        help='Robot model (overrides config)'
    )
    parser.add_argument(
        '--speed',
        type=float,
        default=0.1,
        help='Movement speed (default: 0.1)'
    )
    parser.add_argument(
        '--rate',
        type=float,
        default=100.0,
        help='Control update rate in Hz (default: 100)'
    )
    parser.add_argument(
        '--log-level',
        type=str,
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help='Logging level'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    
    # Load configuration
    config = ConfigLoader.load_robot_config(args.config)
    
    # Override with command line arguments
    robot_ip = args.ip or config['robot']['ip']
    robot_model = args.model or config['robot']['model']
    
    logger.info("=" * 60)
    logger.info("RealMan Robot Keyboard Teleoperation")
    logger.info("=" * 60)
    logger.info(f"Robot IP: {robot_ip}")
    logger.info(f"Robot Model: {robot_model}")
    logger.info(f"Update Rate: {args.rate} Hz")
    logger.info(f"Speed: {args.speed}")
    logger.info("=" * 60)
    
    # Create robot controller
    robot = RobotController(
        ip=robot_ip,
        port=config['robot']['port'],
        model=robot_model
    )
    
    # Connect to robot
    if not robot.connect():
        logger.error("Failed to connect to robot. Exiting.")
        return 1
    
    try:
        # Create keyboard teleoperation
        teleop = KeyboardTeleop(
            robot=robot,
            update_rate=args.rate,
            linear_speed=args.speed,
            angular_speed=args.speed * 3.0,  # Angular typically faster
        )
        
        logger.info("\n" + "=" * 60)
        logger.info("KEYBOARD CONTROLS")
        logger.info("=" * 60)
        logger.info("Movement:")
        logger.info("  W/S: Forward/Backward")
        logger.info("  A/D: Left/Right")
        logger.info("  Q/E: Up/Down")
        logger.info("\nRotation:")
        logger.info("  I/K: Pitch")
        logger.info("  J/L: Roll")
        logger.info("  U/O: Yaw")
        logger.info("\nControl:")
        logger.info("  SHIFT: Hold to enable motion (DEADMAN SWITCH)")
        logger.info("  SPACE: Emergency stop")
        logger.info("  TAB: Switch mode (Cartesian/Joint)")
        logger.info("  +/-: Increase/Decrease speed")
        logger.info("  H: Move to home position")
        logger.info("=" * 60)
        logger.info("\n⚠️  WARNING: Robot will move when SHIFT is held!")
        logger.info("Press Ctrl+C to quit\n")
        
        # Run teleoperation
        teleop.run()
        
    except KeyboardInterrupt:
        logger.info("\nShutting down...")
    
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        return 1
    
    finally:
        # Disconnect from robot
        robot.disconnect()
        logger.info("Disconnected. Goodbye!")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
