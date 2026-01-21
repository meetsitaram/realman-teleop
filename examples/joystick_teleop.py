#!/usr/bin/env python3
"""
Joystick Teleoperation Example

Control RealMan robot with gamepad/joystick.
"""

import sys
import argparse
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from realman_teleop import RobotController, JoystickTeleop
from realman_teleop.config_loader import ConfigLoader
from realman_teleop.utils import setup_logging


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="RealMan Robot Joystick Teleoperation")
    parser.add_argument(
        '--config',
        type=str,
        default='config/robot_config.yaml',
        help='Path to robot configuration file'
    )
    parser.add_argument(
        '--joystick-config',
        type=str,
        default='config/joystick_config.yaml',
        help='Path to joystick configuration file'
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
        '--device',
        type=int,
        default=0,
        help='Joystick device index (default: 0)'
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
    joy_config = ConfigLoader.load_joystick_config(args.joystick_config)
    
    # Override with command line arguments
    robot_ip = args.ip or config['robot']['ip']
    robot_model = args.model or config['robot']['model']
    
    logger.info("=" * 60)
    logger.info("RealMan Robot Joystick Teleoperation")
    logger.info("=" * 60)
    logger.info(f"Robot IP: {robot_ip}")
    logger.info(f"Robot Model: {robot_model}")
    logger.info(f"Joystick Device: {args.device}")
    logger.info(f"Update Rate: {args.rate} Hz")
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
        # Create joystick teleoperation
        teleop = JoystickTeleop(
            robot=robot,
            update_rate=args.rate,
            device_index=args.device,
            axis_map=joy_config.get('joystick', {}).get('axes'),
            button_map=joy_config.get('joystick', {}).get('buttons'),
            deadzone=joy_config.get('joystick', {}).get('deadzone', 0.1),
            normal_speed=joy_config.get('speeds', {}).get('normal', {}).get('linear', 0.1),
            turbo_speed=joy_config.get('speeds', {}).get('turbo', {}).get('linear', 0.3),
        )
        
        logger.info("\n" + "=" * 60)
        logger.info("JOYSTICK CONTROLS")
        logger.info("=" * 60)
        logger.info("Left Stick:")
        logger.info("  Horizontal: Move left/right")
        logger.info("  Vertical: Move forward/backward")
        logger.info("\nRight Stick:")
        logger.info("  Controls rotation and vertical movement")
        logger.info("\nButtons:")
        logger.info("  LB/L1: Hold to enable motion (DEADMAN SWITCH)")
        logger.info("  RB/R1: Hold for turbo speed")
        logger.info("  Back/Select: Emergency stop")
        logger.info("  Start: Switch mode (Cartesian/Joint)")
        logger.info("  B/Circle: Move to home position")
        logger.info("=" * 60)
        logger.info("\n⚠️  WARNING: Robot will move when LB/L1 is held!")
        logger.info("Press Ctrl+C or emergency stop button to quit\n")
        
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
