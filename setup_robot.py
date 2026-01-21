#!/usr/bin/env python3
"""
Robot Setup Script

Interactive script to configure your robot's IP and settings.
Creates .env file with your configuration.
"""

import os
import sys
import subprocess
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)

def print_success(text):
    """Print success message."""
    print(f"✓ {text}")

def print_error(text):
    """Print error message."""
    print(f"✗ {text}")

def print_warning(text):
    """Print warning message."""
    print(f"⚠ {text}")

def test_ping(ip_address):
    """Test if robot IP is reachable."""
    try:
        # Use platform-specific ping command
        if sys.platform.startswith('win'):
            result = subprocess.run(['ping', '-n', '1', '-w', '1000', ip_address], 
                                  capture_output=True, timeout=2)
        else:
            result = subprocess.run(['ping', '-c', '1', '-W', '1', ip_address], 
                                  capture_output=True, timeout=2)
        return result.returncode == 0
    except Exception:
        return False

def detect_robot_dof(ip, port, model):
    """
    Connect to robot and detect DOF (Degrees of Freedom).
    
    Returns:
        int: Number of joints (DOF), or None if detection failed
    """
    try:
        from realman_teleop import RobotController
        
        print("\n  Connecting to robot to detect DOF...")
        robot = RobotController(ip=ip, port=int(port), model=model)
        
        if not robot.connect():
            print_warning("Could not connect to robot for DOF detection")
            return None
        
        # Read joint state to detect DOF
        joints = robot.get_current_joint_angles()
        robot.disconnect()
        
        if joints:
            dof = len(joints)
            print_success(f"Detected {dof} joints (DOF)")
            return dof
        else:
            print_warning("Could not read joint state for DOF detection")
            return None
            
    except Exception as e:
        print_warning(f"DOF detection failed: {e}")
        return None

def main():
    """Main setup function."""
    print_header("RealMan Robot Setup Wizard")
    print("\nThis wizard will help you configure your robot connection.")
    print("Your settings will be saved and automatically used by all scripts.")
    
    project_root = Path(__file__).parent
    config_file = project_root / "robot.yaml"
    
    # Check if robot.yaml already exists
    if config_file.exists():
        print_warning(f"robot.yaml file already exists at: {config_file}")
        response = input("Do you want to reconfigure? (y/N): ").strip().lower()
        if response not in ['y', 'yes']:
            print("\nSetup cancelled. Your existing configuration is unchanged.")
            return 0
        print("\nReconfiguring...")
    
    print("\n" + "-" * 60)
    print("Step 1: Robot Connection")
    print("-" * 60)
    
    # Get robot IP
    while True:
        default_ip = "192.168.10.18"
        ip_input = input(f"\nEnter robot IP address [{default_ip}]: ").strip()
        robot_ip = ip_input if ip_input else default_ip
        
        # Validate IP format (basic)
        parts = robot_ip.split('.')
        if len(parts) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in parts):
            print(f"\nTesting connection to {robot_ip}...")
            if test_ping(robot_ip):
                print_success(f"Robot is reachable at {robot_ip}")
                break
            else:
                print_warning(f"Cannot ping {robot_ip}")
                response = input("Continue anyway? (y/N): ").strip().lower()
                if response in ['y', 'yes']:
                    print_warning("Proceeding without connectivity test")
                    break
                print("Please check your connection and try again.")
        else:
            print_error("Invalid IP address format. Please use format: xxx.xxx.xxx.xxx")
    
    # Get robot port
    default_port = "8080"
    port_input = input(f"\nEnter robot port [{default_port}]: ").strip()
    robot_port = port_input if port_input else default_port
    
    # Get robot model
    print("\nAvailable robot models:")
    models = ["RM65", "RM75", "RML63", "ECO65", "GEN72", "R1D2"]
    for i, model in enumerate(models, 1):
        print(f"  {i}. {model}")
    
    while True:
        default_model = "R1D2"
        model_input = input(f"\nEnter robot model [{default_model}]: ").strip().upper()
        robot_model = model_input if model_input else default_model
        
        if robot_model in models or model_input.isdigit() and 1 <= int(model_input) <= len(models):
            if model_input.isdigit():
                robot_model = models[int(model_input) - 1]
            break
        else:
            print_error(f"Invalid model. Choose from: {', '.join(models)}")
    
    # Detect DOF (Degrees of Freedom)
    print("\n" + "-" * 60)
    print("Step 1b: Detecting Robot Configuration")
    print("-" * 60)
    
    robot_dof = detect_robot_dof(robot_ip, robot_port, robot_model)
    
    if robot_dof is None:
        print_warning("Could not auto-detect DOF")
        print("You can manually specify DOF (typically 6 or 7)")
        dof_input = input("Enter DOF (leave empty to skip): ").strip()
        if dof_input and dof_input.isdigit():
            robot_dof = int(dof_input)
        else:
            robot_dof = None
    
    print("\n" + "-" * 60)
    print("Step 2: Control Settings")
    print("-" * 60)
    
    # Get default speed
    default_speed = "0.1"
    speed_input = input(f"\nDefault movement speed (m/s) [{default_speed}]: ").strip()
    movement_speed = speed_input if speed_input else default_speed
    
    # Get update rate
    default_rate = "100"
    rate_input = input(f"\nControl update rate (Hz) [{default_rate}]: ").strip()
    update_rate = rate_input if rate_input else default_rate
    
    # Get log level
    print("\nLog levels: DEBUG, INFO, WARNING, ERROR")
    default_log = "INFO"
    log_input = input(f"Log level [{default_log}]: ").strip().upper()
    log_level = log_input if log_input in ["DEBUG", "INFO", "WARNING", "ERROR"] else default_log
    
    # Create robot.yaml file
    print("\n" + "-" * 60)
    print("Step 3: Saving Configuration")
    print("-" * 60)
    
    # Build YAML content
    config_data = {
        'robot': {
            'ip': robot_ip,
            'port': int(robot_port),
            'model': robot_model,
        },
        'control': {
            'default_speed': float(movement_speed),
            'default_update_rate': int(update_rate),
        },
        'logging': {
            'level': log_level,
        }
    }
    
    # Add DOF if detected
    if robot_dof is not None:
        config_data['robot']['dof'] = robot_dof
    
    try:
        import yaml
        with open(config_file, 'w') as f:
            f.write("# RealMan Robot Configuration\n")
            f.write("# Generated by setup_robot.py\n")
            f.write("# Edit this file to change your robot settings\n\n")
            yaml.dump(config_data, f, default_flow_style=False, sort_keys=False)
        print_success(f"Configuration saved to: {config_file}")
    except Exception as e:
        print_error(f"Failed to save configuration: {e}")
        return 1
    
    # Also update robot_config.yaml if it exists
    config_file = project_root / "config" / "robot_config.yaml"
    if config_file.exists():
        try:
            import yaml
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
            
            config['robot']['ip'] = robot_ip
            config['robot']['port'] = int(robot_port)
            config['robot']['model'] = robot_model
            if robot_dof is not None:
                config['robot']['dof'] = robot_dof
            
            with open(config_file, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)
            
            print_success(f"Also updated: {config_file}")
        except Exception as e:
            print_warning(f"Could not update robot_config.yaml: {e}")
    
    # Summary
    print_header("Setup Complete!")
    print("\nYour robot configuration:")
    print(f"  IP Address: {robot_ip}")
    print(f"  Port: {robot_port}")
    print(f"  Model: {robot_model}")
    if robot_dof:
        print(f"  DOF (Joints): {robot_dof}")
    print(f"  Default Speed: {movement_speed} m/s")
    print(f"  Update Rate: {update_rate} Hz")
    
    print("\n" + "=" * 60)
    print("Next Steps:")
    print("=" * 60)
    print("\n1. Test connection:")
    print("   python examples/basic_usage.py")
    print("\n2. Start keyboard teleoperation:")
    print("   python examples/keyboard_teleop.py")
    print("   or simply: ./teleop keyboard")
    print("\n3. Start joystick teleoperation:")
    print("   python examples/joystick_teleop.py")
    print("   or simply: ./teleop joystick")
    
    print("\n💡 Tip: You no longer need to pass --ip or --model!")
    print("   All scripts will automatically use your saved settings.")
    
    print("\n🔧 To change settings later:")
    print("   - Run this script again: python setup_robot.py")
    print("   - Or edit directly: nano robot.yaml")
    
    print("\n" + "=" * 60)
    
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(1)

