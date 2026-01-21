#!/usr/bin/env python3
"""
Verify Setup Script

Quick verification that the environment is correctly set up.
"""

import sys
import importlib.util

def check_module(module_name, display_name=None):
    """Check if a Python module is installed."""
    if display_name is None:
        display_name = module_name
    
    spec = importlib.util.find_spec(module_name)
    if spec is not None:
        try:
            module = importlib.import_module(module_name)
            version = getattr(module, '__version__', 'unknown')
            print(f"✓ {display_name:20s} - installed (version: {version})")
            return True
        except ImportError as e:
            print(f"✗ {display_name:20s} - import error: {e}")
            return False
    else:
        print(f"✗ {display_name:20s} - not found")
        return False

def main():
    """Main verification function."""
    print("=" * 60)
    print("RealMan Teleoperation - Setup Verification")
    print("=" * 60)
    print()
    
    print("Python Version:")
    print(f"  {sys.version}")
    print()
    
    print("Checking Dependencies:")
    print("-" * 60)
    
    all_ok = True
    
    # Core dependencies
    all_ok &= check_module("numpy", "NumPy")
    all_ok &= check_module("yaml", "PyYAML")
    all_ok &= check_module("pygame", "Pygame")
    all_ok &= check_module("keyboard", "Keyboard")
    all_ok &= check_module("inputs", "Inputs")
    
    # Optional but recommended
    all_ok &= check_module("scipy", "SciPy")
    all_ok &= check_module("rich", "Rich")
    all_ok &= check_module("colorama", "Colorama")
    
    # RealMan API
    print()
    print("RealMan API:")
    print("-" * 60)
    try:
        from Robotic_Arm.rm_robot_interface import RoboticArm
        print("✓ Robotic_Arm       - installed")
        print("  Successfully imported RoboticArm class")
    except ImportError as e:
        print(f"✗ Robotic_Arm       - import error")
        print(f"  Error: {e}")
        print()
        print("  To install RealMan API:")
        print("    pip install Robotic_Arm")
        all_ok = False
    
    print()
    print("Checking Project Structure:")
    print("-" * 60)
    
    import os
    from pathlib import Path
    
    project_root = Path(__file__).parent
    
    required_dirs = [
        "realman_teleop",
        "examples",
        "config",
        "docs"
    ]
    
    required_files = [
        "realman_teleop/__init__.py",
        "realman_teleop/robot_controller.py",
        "realman_teleop/keyboard_teleop.py",
        "realman_teleop/joystick_teleop.py",
        "config/robot_config.example.yaml",
        "examples/keyboard_teleop.py",
        "examples/joystick_teleop.py",
    ]
    
    for dir_name in required_dirs:
        path = project_root / dir_name
        if path.exists() and path.is_dir():
            print(f"✓ {dir_name:30s} - found")
        else:
            print(f"✗ {dir_name:30s} - missing")
            all_ok = False
    
    print()
    for file_name in required_files:
        path = project_root / file_name
        if path.exists() and path.is_file():
            print(f"✓ {file_name:40s} - found")
        else:
            print(f"✗ {file_name:40s} - missing")
            all_ok = False
    
    print()
    print("Checking Configuration Files:")
    print("-" * 60)
    
    config_files = [
        ("config/robot_config.yaml", "Robot configuration"),
        ("config/keyboard_config.yaml", "Keyboard configuration"),
        ("config/joystick_config.yaml", "Joystick configuration"),
    ]
    
    for config_file, description in config_files:
        path = project_root / config_file
        if path.exists():
            print(f"✓ {description:30s} - exists")
        else:
            example_path = project_root / f"{config_file.replace('.yaml', '.example.yaml')}"
            if example_path.exists():
                print(f"⚠ {description:30s} - not configured (example exists)")
                print(f"  Run: cp {example_path} {path}")
            else:
                print(f"✗ {description:30s} - missing")
    
    print()
    print("=" * 60)
    
    if all_ok:
        print("✅ All checks passed! Setup is complete.")
        print()
        print("Next steps:")
        print("  1. Configure your robot IP in config/robot_config.yaml")
        print("  2. Test connection: python examples/basic_usage.py")
        print("  3. Start teleoperation: python examples/keyboard_teleop.py --model R1D2")
    else:
        print("❌ Some checks failed. Please review the errors above.")
        print()
        print("To fix missing dependencies:")
        print("  conda activate realman-teleop")
        print("  pip install -r requirements.txt")
        return 1
    
    print("=" * 60)
    return 0

if __name__ == '__main__':
    sys.exit(main())

