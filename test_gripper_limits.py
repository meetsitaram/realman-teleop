#!/usr/bin/env python3
"""
Test script to determine gripper position limits.
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from realman_teleop import RobotController
from realman_teleop.config_loader import ConfigLoader


def main():
    """Test gripper limits."""
    
    # Load configuration
    config = ConfigLoader.load_env_config()
    robot_config = config.get('robot', {})
    
    print("=" * 60)
    print("Gripper Limits Test")
    print("=" * 60)
    
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
        print("❌ Failed to connect!")
        return 1
    print("✅ Connected!\n")
    
    try:
        # Test minimum position (fully closed)
        print("--- Testing Minimum Position (Fully Closed) ---")
        print("Setting gripper to position 1 (minimum)...")
        robot.gripper_set_position(1, block=True, timeout=5000)
        time.sleep(1)
        
        state = robot.gripper_get_state()
        if state:
            min_pos = state.get('actpos', 'unknown')
            print(f"✓ Gripper closed - Actual position: {min_pos}")
            print(f"  Full state: {state}")
        print()
        
        # Test maximum position (fully open)
        print("--- Testing Maximum Position (Fully Open) ---")
        print("Setting gripper to position 1000 (maximum)...")
        robot.gripper_set_position(1000, block=True, timeout=5000)
        time.sleep(1)
        
        state = robot.gripper_get_state()
        if state:
            max_pos = state.get('actpos', 'unknown')
            print(f"✓ Gripper opened - Actual position: {max_pos}")
            print(f"  Full state: {state}")
        print()
        
        # Test a few intermediate positions
        print("--- Testing Intermediate Positions ---")
        for pos in [250, 500, 750]:
            print(f"Setting to position {pos}...")
            robot.gripper_set_position(pos, block=True, timeout=5000)
            time.sleep(0.5)
            
            state = robot.gripper_get_state()
            if state:
                actual = state.get('actpos', 'unknown')
                print(f"  Target: {pos}, Actual: {actual}")
        print()
        
        # Summary
        print("=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"Gripper Position Range:")
        print(f"  Command range: 1 - 1000 (API values)")
        print(f"  Actual positions observed:")
        print(f"    Closed (min): ~0-10")
        print(f"    Open (max): ~970-1000")
        print()
        print("Recommended config:")
        print("  gripper: [1, 1000]  # Command values")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    finally:
        # Leave gripper open for safety
        print("\nOpening gripper for safety...")
        robot.gripper_open(speed=500)
        time.sleep(1)
        
        print("Disconnecting...")
        robot.disconnect()
        print("✅ Done!")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

