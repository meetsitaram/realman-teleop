#!/usr/bin/env python3
"""
Joint Limits Test Script

Tests individual joint movement from min to max value using configured limits.
"""

import sys
import time
import argparse
from pathlib import Path
import yaml

sys.path.insert(0, str(Path(__file__).parent.parent))

from realman_teleop import RobotController
from realman_teleop.config_loader import ConfigLoader


def load_joint_limits(config_path: str = None) -> dict:
    """Load joint limits from config file."""
    if config_path is None:
        # Try to find the limits config
        project_root = Path(__file__).parent.parent
        config_path = project_root / "config" / "realman_r1d2_joint_limits.yaml"
    
    config_path = Path(config_path)
    if not config_path.exists():
        print(f"❌ Config file not found: {config_path}")
        return None
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    return config.get('joint_limits', {})


def test_joint_movement(robot: RobotController, joint_num: int, min_val: float, max_val: float, speed: int = 10) -> bool:
    """
    Test moving a joint from min to max value.
    
    Args:
        robot: RobotController instance
        joint_num: Joint number (1-based)
        min_val: Minimum joint angle (degrees)
        max_val: Maximum joint angle (degrees)
        speed: Movement speed (1-100)
        
    Returns:
        True if test passed, False otherwise
    """
    joint_idx = joint_num - 1  # Convert to 0-based index
    
    print(f"\n{'='*60}")
    print(f"Testing Joint {joint_num}")
    print(f"{'='*60}")
    print(f"Configured limits: [{min_val}°, {max_val}°]")
    print(f"Movement speed: {speed}%")
    print()
    
    try:
        # Get current joint angles
        print("Reading current joint angles...")
        current_angles = robot.get_current_joint_angles()
        if not current_angles:
            print("❌ Failed to read current joint angles")
            return False
        
        print(f"Current angles: {[f'{a:.1f}°' for a in current_angles]}")
        print(f"Joint {joint_num} current position: {current_angles[joint_idx]:.2f}°")
        print()
        
        # Create target positions
        target_angles = current_angles.copy()
        
        # Test 1: Move to minimum
        print(f"--- Test 1: Moving Joint {joint_num} to MINIMUM ({min_val}°) ---")
        target_angles[joint_idx] = min_val
        print(f"Target: {[f'{a:.1f}°' for a in target_angles]}")
        
        result = robot.movej(target_angles, velocity=speed, block=True)
        if result != 0:
            print(f"❌ Movement to minimum failed with code: {result}")
            return False
        
        time.sleep(0.5)
        
        # Verify position
        actual_angles = robot.get_current_joint_angles()
        if actual_angles:
            actual_pos = actual_angles[joint_idx]
            error = abs(actual_pos - min_val)
            print(f"✓ Reached minimum")
            print(f"  Target: {min_val:.2f}°, Actual: {actual_pos:.2f}°, Error: {error:.2f}°")
            
            if error > 2.0:  # Allow 2 degree tolerance
                print(f"⚠ Warning: Position error exceeds 2°")
        print()
        
        time.sleep(1)
        
        # Test 2: Move to maximum
        print(f"--- Test 2: Moving Joint {joint_num} to MAXIMUM ({max_val}°) ---")
        target_angles[joint_idx] = max_val
        print(f"Target: {[f'{a:.1f}°' for a in target_angles]}")
        
        result = robot.movej(target_angles, velocity=speed, block=True)
        if result != 0:
            print(f"❌ Movement to maximum failed with code: {result}")
            return False
        
        time.sleep(0.5)
        
        # Verify position
        actual_angles = robot.get_current_joint_angles()
        if actual_angles:
            actual_pos = actual_angles[joint_idx]
            error = abs(actual_pos - max_val)
            print(f"✓ Reached maximum")
            print(f"  Target: {max_val:.2f}°, Actual: {actual_pos:.2f}°, Error: {error:.2f}°")
            
            if error > 2.0:
                print(f"⚠ Warning: Position error exceeds 2°")
        print()
        
        time.sleep(1)
        
        # Test 3: Move to center
        center_val = (min_val + max_val) / 2
        print(f"--- Test 3: Moving Joint {joint_num} to CENTER ({center_val:.1f}°) ---")
        target_angles[joint_idx] = center_val
        
        result = robot.movej(target_angles, velocity=speed, block=True)
        if result != 0:
            print(f"❌ Movement to center failed with code: {result}")
            return False
        
        time.sleep(0.5)
        
        actual_angles = robot.get_current_joint_angles()
        if actual_angles:
            actual_pos = actual_angles[joint_idx]
            error = abs(actual_pos - center_val)
            print(f"✓ Reached center")
            print(f"  Target: {center_val:.2f}°, Actual: {actual_pos:.2f}°, Error: {error:.2f}°")
        print()
        
        print(f"{'='*60}")
        print(f"✅ Joint {joint_num} test PASSED")
        print(f"{'='*60}")
        
        return True
        
    except Exception as e:
        print(f"❌ Exception during test: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Test individual joint limits by moving from min to max",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test joint 1
  python test_joint_limits.py --joint 1
  
  # Test joint 3 with slower speed
  python test_joint_limits.py --joint 3 --speed 5
  
  # Use custom config file
  python test_joint_limits.py --joint 2 --config my_limits.yaml
        """
    )
    
    parser.add_argument(
        '--joint',
        type=int,
        required=True,
        help='Joint number to test (1-6 or 1-7 depending on robot)'
    )
    
    parser.add_argument(
        '--speed',
        type=int,
        default=10,
        help='Movement speed (1-100, default: 10 for safety)'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        help='Path to joint limits config file (default: config/realman_r1d2_joint_limits.yaml)'
    )
    
    args = parser.parse_args()
    
    # Load joint limits
    print("=" * 60)
    print("Joint Limits Test")
    print("=" * 60)
    print()
    
    joint_limits = load_joint_limits(args.config)
    if not joint_limits:
        return 1
    
    print("Loaded joint limits:")
    for joint_name, limits in joint_limits.items():
        print(f"  {joint_name}: {limits}")
    print()
    
    # Get limits for requested joint
    joint_key = f"joint_{args.joint}"
    if joint_key not in joint_limits:
        print(f"❌ Joint {args.joint} not found in config!")
        print(f"Available joints: {', '.join(joint_limits.keys())}")
        return 1
    
    min_val, max_val = joint_limits[joint_key]
    
    # Validate speed
    if args.speed < 1 or args.speed > 100:
        print(f"❌ Speed must be between 1 and 100")
        return 1
    
    # Load robot configuration
    config = ConfigLoader.load_env_config()
    robot_config = config.get('robot', {})
    
    print(f"Robot Configuration:")
    print(f"  IP: {robot_config.get('ip', '192.168.10.18')}")
    print(f"  Model: {robot_config.get('model', 'R1D2')}")
    print(f"  DOF: {robot_config.get('dof', 'auto-detect')}")
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
    
    # Safety check
    print()
    print("⚠️  WARNING: The robot will move!")
    print(f"    Joint {args.joint} will move from {min_val}° to {max_val}°")
    print()
    response = input("Continue with test? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("Test cancelled.")
        robot.disconnect()
        return 0
    
    try:
        # Run the test
        success = test_joint_movement(
            robot=robot,
            joint_num=args.joint,
            min_val=min_val,
            max_val=max_val,
            speed=args.speed
        )
        
        print()
        if success:
            print("✅ All tests passed!")
            return 0
        else:
            print("❌ Test failed!")
            return 1
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user!")
        return 1
    
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    finally:
        print("\nDisconnecting...")
        robot.disconnect()
        print("✅ Done!")


if __name__ == '__main__':
    sys.exit(main())


