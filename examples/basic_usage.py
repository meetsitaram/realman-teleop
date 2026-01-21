#!/usr/bin/env python3
"""
Simple Python API Usage Example

Demonstrates basic usage of the realman_teleop library.
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from realman_teleop import RobotController
from realman_teleop.config_loader import ConfigLoader
import time


def main():
    """Demonstrate basic robot control."""
    
    # Load configured settings from .env file
    config = ConfigLoader.load_env_config()
    robot_config = config.get('robot', {})
    
    parser = argparse.ArgumentParser(
        description="Basic RealMan Robot Control Example",
        epilog="Settings are loaded from .env file. Run 'python setup_robot.py' to configure."
    )
    parser.add_argument(
        '--ip',
        type=str,
        default=robot_config.get('ip', '192.168.10.18'),
        help=f"Robot IP address (default from .env: {robot_config.get('ip', '192.168.10.18')})"
    )
    parser.add_argument(
        '--model',
        type=str,
        default=robot_config.get('model', 'RM65'),
        choices=['RM65', 'RM75', 'RML63', 'ECO65', 'GEN72', 'R1D2'],
        help=f"Robot model (default from .env: {robot_config.get('model', 'RM65')})"
    )
    parser.add_argument(
        '--port',
        type=int,
        default=robot_config.get('port', 8080),
        help=f"Robot port (default from .env: {robot_config.get('port', 8080)})"
    )
    parser.add_argument(
        '--dof',
        type=int,
        choices=[6, 7],
        help='Robot degrees of freedom (6 or 7). Auto-detects if not specified.'
    )
    
    args = parser.parse_args()
    
    # Get DOF from args, config, or let it auto-detect
    dof = args.dof or robot_config.get('dof', None)
    
    # Create robot controller
    print("=" * 60)
    print("RealMan Robot - Basic API Example")
    print("=" * 60)
    print(f"Robot IP: {args.ip}")
    print(f"Robot Model: {args.model}")
    print(f"Robot Port: {args.port}")
    if dof:
        print(f"Robot DOF: {dof} (configured)")
    else:
        print(f"Robot DOF: Auto-detect")
    print()
    print("ℹ️  Settings loaded from .env file")
    print("   To change defaults, run: python setup_robot.py")
    print("=" * 60)
    print()
    
    print("Creating robot controller...")
    robot = RobotController(
        ip=args.ip,
        port=args.port,
        model=args.model,
        dof=dof
    )
    
    # Connect to robot
    print("Connecting to robot...")
    if not robot.connect():
        print("Failed to connect!")
        return 1
    
    print("Connected successfully!")
    
    try:
        # Get current state
        print("\n--- Current Robot State ---")
        joints = robot.get_current_joint_angles()
        print(f"Joint angles: {joints}")
        
        pose = robot.get_current_pose()
        print(f"End-effector pose: {pose}")
        
        if not joints or not pose:
            print("Error: Could not read robot state")
            return 1
        
        # Move joints by small offset (safer than absolute positions)
        print("\n--- Moving joints by +5 degrees ---")
        target_joints = [j + 5.0 for j in joints]
        print(f"Current: {[f'{j:.2f}' for j in joints]}")
        print(f"Target:  {[f'{j:.2f}' for j in target_joints]}")
        robot.movej(target_joints, velocity=20, block=True)
        time.sleep(1)
        
        # Move back by reading current and subtracting
        print("\n--- Moving joints by -5 degrees (back to start) ---")
        current_joints = robot.get_current_joint_angles()
        if current_joints:
            target_joints = [j - 5.0 for j in current_joints]
            print(f"Current: {[f'{j:.2f}' for j in current_joints]}")
            print(f"Target:  {[f'{j:.2f}' for j in target_joints]}")
            robot.movej(target_joints, velocity=20, block=True)
            time.sleep(1)
        
        # Move in Cartesian space by small offset
        print("\n--- Moving in Cartesian space ---")
        current_pose = robot.get_current_pose()
        if current_pose:
            # Move 5cm up (in Z direction) - safer than X/Y movement
            target_pose = current_pose.copy()
            target_pose[2] += 0.05  # 5cm up
            print(f"Current Z: {current_pose[2]:.4f}m")
            print(f"Target Z:  {target_pose[2]:.4f}m (+5cm)")
            robot.movel(target_pose, velocity=20, block=True)
            time.sleep(1)
            
            # Move back down
            print("\n--- Moving back down ---")
            target_pose[2] -= 0.05  # Back down
            print(f"Target Z:  {target_pose[2]:.4f}m")
            robot.movel(target_pose, velocity=20, block=True)
        
        print("\n--- Success! ---")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    finally:
        # Disconnect
        print("\nDisconnecting...")
        robot.disconnect()
        print("Done!")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
