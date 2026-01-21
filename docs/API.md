# API Documentation

## RobotController

Main interface for controlling RealMan robotic arms.

### Initialization

```python
from realman_teleop import RobotController

robot = RobotController(
    ip="192.168.1.18",
    port=8080,
    model="RM65"
)
```

### Connection Management

```python
# Connect to robot
robot.connect()

# Disconnect from robot
robot.disconnect()

# Context manager (automatically connects/disconnects)
with RobotController(ip="192.168.1.18", model="RM65") as robot:
    # Your code here
    pass
```

### Motion Commands

```python
# Move joints to specific angles (degrees)
robot.movej([0, 20, 70, 0, 90, 0], velocity=20, block=True)

# Move to Cartesian pose using joint interpolation
robot.movej_p([0.3, 0, 0.3, 3.14, 0, 0], velocity=20, block=True)

# Move to Cartesian pose using linear interpolation
robot.movel([0.3, 0, 0.3, 3.14, 0, 0], velocity=20, block=True)

# Emergency stop
robot.stop()

# Move to home position
robot.move_to_home(velocity=20)
```

### State Queries

```python
# Get current joint angles (degrees)
joints = robot.get_current_joint_angles()

# Get current end-effector pose [x, y, z, rx, ry, rz]
pose = robot.get_current_pose()

# Get joint velocities (deg/s)
velocities = robot.get_joint_velocities()

# Check if robot is moving
is_moving = robot.is_moving()
```

### Safety

```python
# Set collision detection level (0-8)
robot.set_collision_level(3)

# Clear error state
robot.clear_errors()
```

## KeyboardTeleop

Keyboard-based teleoperation interface.

### Initialization

```python
from realman_teleop import RobotController, KeyboardTeleop

robot = RobotController(ip="192.168.1.18", model="RM65")
robot.connect()

teleop = KeyboardTeleop(
    robot=robot,
    update_rate=100.0,
    linear_speed=0.1,
    angular_speed=0.3
)
```

### Running

```python
# Start teleoperation (blocking)
teleop.run()

# Or in a separate thread
import threading
thread = threading.Thread(target=teleop.run)
thread.start()

# Stop teleoperation
teleop.stop()
```

### Default Controls

- **W/S**: Forward/Backward
- **A/D**: Left/Right
- **Q/E**: Up/Down
- **I/K**: Pitch rotation
- **J/L**: Roll rotation
- **U/O**: Yaw rotation
- **SHIFT**: Enable (deadman switch)
- **SPACE**: Emergency stop
- **TAB**: Switch mode
- **H**: Go home

## JoystickTeleop

Joystick/gamepad-based teleoperation interface.

### Initialization

```python
from realman_teleop import RobotController, JoystickTeleop

robot = RobotController(ip="192.168.1.18", model="RM65")
robot.connect()

teleop = JoystickTeleop(
    robot=robot,
    update_rate=100.0,
    device_index=0,
    deadzone=0.1,
    normal_speed=0.1,
    turbo_speed=0.3
)
```

### Running

```python
teleop.run()
```

### Default Controls (Xbox Layout)

- **Left Stick**: Linear X/Y movement
- **Right Stick**: Angular/vertical movement
- **LB (L1)**: Enable (deadman switch)
- **RB (R1)**: Turbo mode
- **Back/Select**: Emergency stop
- **Start**: Switch mode
- **B Button**: Go home

## SafetyMonitor

Safety feature monitoring and enforcement.

### Initialization

```python
from realman_teleop.safety import SafetyMonitor

safety = SafetyMonitor(
    robot=robot,
    enable_velocity_limits=True,
    enable_workspace_limits=True,
    enable_collision_detection=True
)
```

### Configuration

```python
# Set velocity limits
safety.set_velocity_limits(
    linear=0.5,    # m/s
    angular=1.0,   # rad/s
    joint=30.0     # deg/s
)

# Set workspace limits
safety.set_workspace_limits({
    'x': (-0.7, 0.7),
    'y': (-0.7, 0.7),
    'z': (0.0, 1.0)
})

# Enable collision detection
safety.enable_collision_detection(level=3)
```

### Usage

```python
# Check commands for safety violations
safe_commands = safety.check_commands(commands)

# Trigger emergency stop
safety.trigger_emergency_stop()

# Reset emergency stop
safety.reset_emergency_stop()
```

## Control Modes

### JointControl

Direct joint angle control.

```python
from realman_teleop.control_modes import JointControl

joint_control = JointControl(max_joint_velocity=30.0)

command = joint_control.compute_command(
    input_velocity=[0, 5, 10, 0, 5, 0],
    current_state={'joint_angles': current_joints, 'dt': 0.01}
)
```

### CartesianControl

End-effector Cartesian space control.

```python
from realman_teleop.control_modes import CartesianControl

cartesian_control = CartesianControl(
    max_linear_velocity=0.5,
    max_angular_velocity=1.0
)

command = cartesian_control.compute_command(
    input_velocity=[0.1, 0, 0, 0, 0, 0.5],
    current_state={'pose': current_pose, 'dt': 0.01}
)
```

### VelocityControl

Continuous velocity control with smoothing.

```python
from realman_teleop.control_modes import VelocityControl

velocity_control = VelocityControl(
    max_velocity=0.5,
    smoothing_factor=0.5
)

command = velocity_control.compute_command(
    input_velocity=[0.1, 0, 0, 0, 0, 0],
    current_state={}
)
```

## Utility Functions

### Logging

```python
from realman_teleop.utils import setup_logging

setup_logging(level="INFO", log_file="robot.log")
```

### Conversions

```python
from realman_teleop.utils import (
    degrees_to_radians,
    radians_to_degrees,
    clamp,
    apply_deadzone
)

radians = degrees_to_radians([0, 90, 180])
degrees = radians_to_degrees([0, 1.57, 3.14])
clamped = clamp(value, min_val=0, max_val=1)
filtered = apply_deadzone(value, deadzone=0.1)
```

## Configuration Loading

```python
from realman_teleop.config_loader import ConfigLoader

# Load robot configuration
robot_config = ConfigLoader.load_robot_config("config/robot_config.yaml")

# Load keyboard configuration
kb_config = ConfigLoader.load_keyboard_config("config/keyboard_config.yaml")

# Load joystick configuration
joy_config = ConfigLoader.load_joystick_config("config/joystick_config.yaml")

# Get default configurations
default_robot = ConfigLoader.get_default_robot_config()
default_keyboard = ConfigLoader.get_default_keyboard_config()
default_joystick = ConfigLoader.get_default_joystick_config()
```
