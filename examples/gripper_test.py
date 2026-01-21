#!/usr/bin/env python3
"""
Gripper Control Test

Simple script to test gripper open/close functionality.
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from realman_teleop import RobotController
from realman_teleop.config_loader import ConfigLoader


def main():
    """Test gripper control."""
    
    # Load configuration
    config = ConfigLoader.load_env_config()
    robot_config = config.get('robot', {})
    
    print("=" * 60)
    print("RealMan Robot - Gripper Control Test")
    print("=" * 60)
    print(f"Robot IP: {robot_config.get('ip', '192.168.10.18')}")
    print(f"Robot Model: {robot_config.get('model', 'R1D2')}")
    print("=" * 60)
    print()
    
    # Create robot controller
    robot = RobotController(
        ip=robot_config.get('ip', '192.168.10.18'),
        port=robot_config.get('port', 8080),
        model=robot_config.get('model', 'R1D2'),
        dof=robot_config.get('dof')
    )
    
    # Connect to robot
    print("Connecting to robot...")
    if not robot.connect():
        print("❌ Failed to connect to robot!")
        return 1
    print("✅ Connected successfully!")
    print()
    
    try:
        # Get initial gripper state
        print("--- Initial Gripper State ---")
        state = robot.gripper_get_state()
        if state:
            print(f"Gripper state: {state}")
        print()
        
        # Test 1: Open gripper
        print("--- Test 1: Opening Gripper ---")
        result = robot.gripper_open(speed=500)
        if result == 0:
            print("✓ Gripper opened successfully")
        else:
            print(f"⚠ Gripper open returned code: {result}")
        time.sleep(2)
        print()
        
        # Test 2: Close gripper with force control
        print("--- Test 2: Closing Gripper (Force Control) ---")
        result = robot.gripper_close(speed=500, force=300)
        if result == 0:
            print("✓ Gripper closed successfully")
        else:
            print(f"⚠ Gripper close returned code: {result}")
        time.sleep(2)
        print()
        
        # Test 3: Set specific position (half open)
        print("--- Test 3: Setting Gripper to Half Open (500) ---")
        result = robot.gripper_set_position(500)
        if result == 0:
            print("✓ Gripper position set successfully")
        else:
            print(f"⚠ Gripper set position returned code: {result}")
        time.sleep(2)
        print()
        
        # Test 4: Fully open again
        print("--- Test 4: Fully Opening Gripper ---")
        result = robot.gripper_open(speed=800)
        if result == 0:
            print("✓ Gripper fully opened")
        else:
            print(f"⚠ Gripper open returned code: {result}")
        print()
        
        # Get final gripper state
        print("--- Final Gripper State ---")
        state = robot.gripper_get_state()
        if state:
            print(f"Gripper state: {state}")
        
        print("\n--- Test Complete! ---")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    finally:
        # Disconnect
        print("\nDisconnecting...")
        robot.disconnect()
        print("✅ Done!")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

