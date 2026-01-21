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
import time


def main():
    """Demonstrate basic robot control."""
    
    parser = argparse.ArgumentParser(description="Basic RealMan Robot Control Example")
    parser.add_argument(
        '--ip',
        type=str,
        default='192.168.1.18',
        help='Robot IP address (default: 192.168.1.18)'
    )
    parser.add_argument(
        '--model',
        type=str,
        default='RM65',
        choices=['RM65', 'RM75', 'RML63', 'ECO65', 'GEN72', 'R1D2'],
        help='Robot model (default: RM65)'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8080,
        help='Robot port (default: 8080)'
    )
    
    args = parser.parse_args()
    
    # Create robot controller
    print("=" * 60)
    print("RealMan Robot - Basic API Example")
    print("=" * 60)
    print(f"Robot IP: {args.ip}")
    print(f"Robot Model: {args.model}")
    print(f"Robot Port: {args.port}")
    print("=" * 60)
    print()
    
    print("Creating robot controller...")
    robot = RobotController(
        ip=args.ip,
        port=args.port,
        model=args.model
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
        
        # Move to home position
        print("\n--- Moving to home position ---")
        robot.move_to_home(velocity=20)
        time.sleep(2)
        
        # Move joints
        print("\n--- Moving joints ---")
        target_joints = [0, 30, 60, 0, 90, 0]
        print(f"Moving to: {target_joints}")
        robot.movej(target_joints, velocity=20, block=True)
        
        # Move in Cartesian space
        print("\n--- Moving in Cartesian space ---")
        current_pose = robot.get_current_pose()
        if current_pose:
            # Move 10cm forward (in X direction)
            target_pose = current_pose.copy()
            target_pose[0] += 0.1
            print(f"Moving to: {target_pose}")
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
