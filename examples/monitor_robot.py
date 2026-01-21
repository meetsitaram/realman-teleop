#!/usr/bin/env python3
"""
Robot State Monitor

Continuously read and display robot state without sending any commands.
Safe way to verify connection before teleoperation.
"""

import sys
import argparse
import logging
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from realman_teleop import RobotController
from realman_teleop.config_loader import ConfigLoader
from realman_teleop.utils import setup_logging

try:
    from rich.console import Console
    from rich.table import Table
    from rich.live import Live
    from rich.panel import Panel
    from rich.layout import Layout
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


def format_joint_angles(joints):
    """Format joint angles for display."""
    if joints is None:
        return "N/A"
    return ", ".join([f"{j:7.2f}°" for j in joints])


def format_pose(pose):
    """Format pose for display."""
    if pose is None:
        return "N/A"
    pos = f"[{pose[0]:6.3f}, {pose[1]:6.3f}, {pose[2]:6.3f}] m"
    rot = f"[{pose[3]:6.3f}, {pose[4]:6.3f}, {pose[5]:6.3f}] rad"
    return f"Pos: {pos}\n     Rot: {rot}"


def format_velocities(velocities):
    """Format velocities for display."""
    if velocities is None:
        return "N/A"
    return ", ".join([f"{v:7.2f}°/s" for v in velocities])


def monitor_with_rich(robot, update_rate=10):
    """Monitor robot state with rich terminal UI."""
    console = Console()
    
    with Live(console=console, refresh_per_second=update_rate) as live:
        try:
            while True:
                # Get robot state
                joints = robot.get_current_joint_angles()
                pose = robot.get_current_pose()
                velocities = robot.get_joint_velocities()
                is_moving = robot.is_moving()
                
                # Create display table
                table = Table(title="🤖 Robot State Monitor", show_header=True, header_style="bold magenta")
                table.add_column("Property", style="cyan", width=20)
                table.add_column("Value", style="green")
                
                # Add robot info
                table.add_row("Robot Model", robot.model_name)
                table.add_row("IP Address", f"{robot.ip}:{robot.port}")
                table.add_row("DOF", str(robot.dof))
                table.add_row("Status", "🟢 Moving" if is_moving else "🟡 Idle")
                
                table.add_section()
                
                # Add joint angles
                if joints:
                    for i, angle in enumerate(joints, 1):
                        table.add_row(f"Joint {i}", f"{angle:8.2f}°")
                
                table.add_section()
                
                # Add pose
                if pose:
                    table.add_row("Position X", f"{pose[0]:8.4f} m")
                    table.add_row("Position Y", f"{pose[1]:8.4f} m")
                    table.add_row("Position Z", f"{pose[2]:8.4f} m")
                    table.add_row("Rotation RX", f"{pose[3]:8.4f} rad")
                    table.add_row("Rotation RY", f"{pose[4]:8.4f} rad")
                    table.add_row("Rotation RZ", f"{pose[5]:8.4f} rad")
                
                table.add_section()
                
                # Add velocities
                if velocities:
                    for i, vel in enumerate(velocities, 1):
                        table.add_row(f"Velocity J{i}", f"{vel:8.2f}°/s")
                
                # Create panel with instructions
                instructions = Panel(
                    "[yellow]Press Ctrl+C to stop monitoring[/yellow]\n"
                    "[dim]This is READ-ONLY mode - no commands are sent to the robot[/dim]",
                    title="Controls",
                    border_style="blue"
                )
                
                # Update display
                layout = Layout()
                layout.split_column(
                    Layout(table, size=len(joints or []) + 15),
                    Layout(instructions, size=4)
                )
                
                live.update(layout)
                time.sleep(1.0 / update_rate)
                
        except KeyboardInterrupt:
            console.print("\n[yellow]Monitoring stopped by user[/yellow]")


def monitor_simple(robot, update_rate=10):
    """Monitor robot state with simple text output."""
    print("=" * 80)
    print("🤖 Robot State Monitor")
    print("=" * 80)
    print(f"Robot Model: {robot.model_name}")
    print(f"IP Address: {robot.ip}:{robot.port}")
    print(f"DOF: {robot.dof}")
    print("=" * 80)
    print("\nPress Ctrl+C to stop monitoring")
    print("This is READ-ONLY mode - no commands are sent to the robot\n")
    
    try:
        while True:
            # Get robot state
            joints = robot.get_current_joint_angles()
            pose = robot.get_current_pose()
            velocities = robot.get_joint_velocities()
            is_moving = robot.is_moving()
            
            # Clear screen (optional)
            print("\033[2J\033[H", end="")  # ANSI escape codes to clear screen
            
            print("=" * 80)
            print(f"Robot State Monitor - {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print("=" * 80)
            
            print(f"\nStatus: {'🟢 Moving' if is_moving else '🟡 Idle'}")
            
            print("\n--- Joint Angles (degrees) ---")
            if joints:
                for i, angle in enumerate(joints, 1):
                    bar = "█" * int(abs(angle) / 10) if abs(angle) < 180 else "█" * 18
                    print(f"  Joint {i}: {angle:8.2f}° {bar}")
            else:
                print("  No data available")
            
            print("\n--- End-Effector Pose ---")
            if pose:
                print(f"  Position: X={pose[0]:7.4f}m  Y={pose[1]:7.4f}m  Z={pose[2]:7.4f}m")
                print(f"  Rotation: RX={pose[3]:7.4f}rad RY={pose[4]:7.4f}rad RZ={pose[5]:7.4f}rad")
            else:
                print("  No data available")
            
            print("\n--- Joint Velocities (deg/s) ---")
            if velocities:
                for i, vel in enumerate(velocities, 1):
                    print(f"  Joint {i}: {vel:8.2f}°/s")
            else:
                print("  No data available")
            
            print("\n" + "=" * 80)
            print("Press Ctrl+C to stop monitoring")
            print("=" * 80)
            
            time.sleep(1.0 / update_rate)
            
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped by user")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Monitor robot state without sending commands (READ-ONLY mode)"
    )
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
        '--dof',
        type=int,
        choices=[6, 7],
        help='Robot degrees of freedom (6 or 7). Auto-detects if not specified.'
    )
    parser.add_argument(
        '--rate',
        type=float,
        default=10.0,
        help='Update rate in Hz (default: 10)'
    )
    parser.add_argument(
        '--simple',
        action='store_true',
        help='Use simple text output instead of rich UI'
    )
    parser.add_argument(
        '--log-level',
        type=str,
        default='WARNING',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help='Logging level (default: WARNING for cleaner output)'
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
    robot_dof = args.dof or config['robot'].get('dof', None)
    
    logger.info("=" * 60)
    logger.info("Robot State Monitor (READ-ONLY)")
    logger.info("=" * 60)
    logger.info(f"Robot IP: {robot_ip}")
    logger.info(f"Robot Model: {robot_model}")
    if robot_dof:
        logger.info(f"Robot DOF: {robot_dof} (configured)")
    else:
        logger.info(f"Robot DOF: Auto-detect")
    logger.info(f"Update Rate: {args.rate} Hz")
    logger.info("=" * 60)
    
    # Create robot controller
    robot = RobotController(
        ip=robot_ip,
        port=config['robot']['port'],
        model=robot_model,
        dof=robot_dof
    )
    
    # Connect to robot
    print(f"\n🔌 Connecting to {robot_model} at {robot_ip}:{config['robot']['port']}...")
    
    if not robot.connect():
        print("❌ Failed to connect to robot!")
        print("\nTroubleshooting:")
        print(f"  1. Check robot is powered on")
        print(f"  2. Verify network connection: ping {robot_ip}")
        print(f"  3. Confirm IP address is correct")
        print(f"  4. Check firewall settings")
        return 1
    
    print("✅ Connected successfully!\n")
    print("📊 Starting state monitor...")
    print("⚠️  READ-ONLY MODE: No commands will be sent to the robot")
    print()
    
    try:
        # Choose display mode
        if RICH_AVAILABLE and not args.simple:
            monitor_with_rich(robot, args.rate)
        else:
            if not RICH_AVAILABLE and not args.simple:
                print("ℹ️  Rich library not available, using simple display")
                print("   Install with: pip install rich")
                print()
            monitor_simple(robot, args.rate)
        
    except KeyboardInterrupt:
        print("\n\n👋 Stopping monitor...")
    
    except Exception as e:
        logger.error(f"Error during monitoring: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")
        return 1
    
    finally:
        # Disconnect from robot
        print("🔌 Disconnecting...")
        robot.disconnect()
        print("✅ Disconnected safely. Goodbye!")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

