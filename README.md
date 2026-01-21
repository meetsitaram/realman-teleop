# RealMan Robot Teleoperation

A Python library for teleoperating RealMan robotic arms using keyboard, joystick, or gamepad inputs. Built on top of the official RealMan RM_API2.

## 🤖 Supported Robot Models

- **RM65 Series**: 6-DOF collaborative robots (RM65-B, RM65-ZF, RM65-6F)
- **RM75 Series**: 7-DOF collaborative robots (RM75-B, RM75-ZF, RM75-6F)
- **RML63 Series**: Long-reach 6-DOF robots (RML63-B, RML63-ZF, RML63-6F)
- **ECO65 Series**: Economical 6-DOF robots (ECO65-B, ECO65-ZF, ECO65-6F)
- **GEN72 Series**: 7-DOF general-purpose robots (GEN72-B, GEN72-ZF, GEN72-6F)
- **R1D2**: Single arm 6-DOF robot

## ✨ Features

- **Multiple Control Modes**:
  - 🎮 Joystick/Gamepad control (Xbox, PS4, PS5, generic USB controllers)
  - ⌨️ Keyboard control for quick testing
  - 🖱️ Mouse control (future)
  - 🤖 ROS integration (future)

- **Control Types**:
  - Joint space control (direct joint angle manipulation)
  - Cartesian space control (position and orientation in 3D space)
  - Velocity control (continuous motion)
  - Force control (for robots with force sensors)

- **Safety Features**:
  - Deadman switch (must hold enable button)
  - Emergency stop
  - Velocity limits
  - Position limits
  - Collision detection integration

- **Configuration**:
  - YAML-based configuration files
  - Per-robot-model presets
  - Custom button/key mappings
  - Adjustable speed profiles

## 📋 Requirements

### Hardware
- RealMan robotic arm (any supported model)
- Computer running Linux (Ubuntu 20.04+ recommended) or Windows 10/11
- Network connection to robot (Ethernet recommended)
- Optional: USB game controller (Xbox, PS4, etc.)

### Software
- Python 3.9 or higher
- RealMan RM_API2 Python package
- Additional Python packages (see requirements.txt)

## 🚀 Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/realman-teleop.git
cd realman-teleop
```

### 2. Install Python dependencies
```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 3. Install RealMan API
```bash
# Option 1: Install from PyPI
pip install Robotic_Arm

# Option 2: Install from source
git clone https://github.com/RealManRobot/RM_API2.git
cd RM_API2/Python
pip install .
```

### 4. Configure your robot
```bash
# Copy example configuration
cp config/robot_config.example.yaml config/robot_config.yaml

# Edit with your robot's IP address and model
nano config/robot_config.yaml
```

## 🎮 Quick Start

### Keyboard Teleoperation
```bash
# Basic keyboard control
python examples/keyboard_teleop.py --config config/robot_config.yaml

# Keyboard control with custom speed
python examples/keyboard_teleop.py --speed 0.5 --config config/robot_config.yaml
```

### Joystick Teleoperation
```bash
# List available joysticks
python examples/list_joysticks.py

# Start joystick control
python examples/joystick_teleop.py --config config/robot_config.yaml

# With custom joystick device
python examples/joystick_teleop.py --device /dev/input/js0 --config config/robot_config.yaml
```

### Python API Usage
```python
from realman_teleop import RobotController, KeyboardTeleop

# Initialize robot connection
robot = RobotController(
    ip="192.168.1.18",
    port=8080,
    model="RM65"
)

# Start keyboard teleoperation
teleop = KeyboardTeleop(robot)
teleop.run()
```

## 📖 Usage Examples

See the `examples/` directory for complete working examples:

- `keyboard_teleop.py` - Basic keyboard control
- `joystick_teleop.py` - Gamepad/joystick control
- `joint_control.py` - Direct joint angle control
- `cartesian_control.py` - Cartesian space control
- `velocity_control.py` - Continuous velocity mode
- `force_control.py` - Force-controlled teleoperation (requires force sensor)
- `custom_mapping.py` - Custom button/key mapping example

## ⚙️ Configuration

### Robot Configuration (robot_config.yaml)
```yaml
robot:
  ip: "192.168.1.18"
  port: 8080
  model: "RM65"  # RM65, RM75, RML63, ECO65, GEN72
  
control:
  mode: "cartesian"  # joint, cartesian, velocity
  update_rate: 100  # Hz
  
limits:
  max_linear_velocity: 0.5  # m/s
  max_angular_velocity: 1.0  # rad/s
  max_joint_velocity: 1.0  # rad/s
  
safety:
  enable_deadman: true
  enable_collision_detection: true
  emergency_stop_enabled: true
```

### Joystick Configuration (joystick_config.yaml)
```yaml
joystick:
  device: "/dev/input/js0"  # Auto-detect if not specified
  deadzone: 0.1
  
axes:
  linear_x: 1  # Left stick vertical
  linear_y: 0  # Left stick horizontal
  linear_z: 4  # Right stick vertical
  angular_x: 3  # Right stick horizontal
  angular_y: 5  # Triggers
  angular_z: 2  # D-pad
  
buttons:
  enable: 4  # L1 button (deadman switch)
  turbo: 5   # R1 button (speed boost)
  emergency_stop: 6  # Select/Back button
  mode_switch: 7  # Start button
  
speeds:
  normal:
    linear: 0.1  # m/s
    angular: 0.3  # rad/s
  turbo:
    linear: 0.3
    angular: 0.8
```

### Keyboard Configuration (keyboard_config.yaml)
```yaml
keyboard:
  # Movement keys
  forward: 'w'
  backward: 's'
  left: 'a'
  right: 'd'
  up: 'q'
  down: 'e'
  
  # Rotation keys
  rotate_x_pos: 'i'
  rotate_x_neg: 'k'
  rotate_y_pos: 'j'
  rotate_y_neg: 'l'
  rotate_z_pos: 'u'
  rotate_z_neg: 'o'
  
  # Control keys
  emergency_stop: 'space'
  enable: 'shift'
  mode_switch: 'tab'
  increase_speed: '+'
  decrease_speed: '-'
  
speeds:
  linear: 0.1  # m/s
  angular: 0.3  # rad/s
```

## 🗂️ Project Structure

```
realman-teleop/
├── README.md
├── LICENSE
├── requirements.txt
├── setup.py
│
├── config/
│   ├── robot_config.example.yaml
│   ├── joystick_config.example.yaml
│   └── keyboard_config.example.yaml
│
├── realman_teleop/
│   ├── __init__.py
│   ├── robot_controller.py      # Main robot control interface
│   ├── teleop_base.py            # Base teleoperation class
│   ├── keyboard_teleop.py        # Keyboard control implementation
│   ├── joystick_teleop.py        # Joystick control implementation
│   ├── control_modes.py          # Joint/Cartesian/Velocity control modes
│   ├── safety.py                 # Safety features (limits, deadman, e-stop)
│   ├── config_loader.py          # Configuration file parser
│   └── utils.py                  # Utility functions
│
├── examples/
│   ├── keyboard_teleop.py
│   ├── joystick_teleop.py
│   ├── joint_control.py
│   ├── cartesian_control.py
│   ├── velocity_control.py
│   ├── force_control.py
│   ├── custom_mapping.py
│   └── list_joysticks.py
│
├── tests/
│   ├── test_robot_controller.py
│   ├── test_keyboard_teleop.py
│   ├── test_joystick_teleop.py
│   └── test_safety.py
│
└── docs/
    ├── API.md
    ├── CONFIGURATION.md
    ├── TROUBLESHOOTING.md
    └── CONTRIBUTING.md
```

## 🔧 Troubleshooting

### Cannot connect to robot
- Verify robot IP address and network connection
- Check that robot controller is powered on
- Ensure firewall allows connection on port 8080
- Try pinging the robot: `ping 192.168.1.18`

### Joystick not detected
- Check USB connection
- List devices: `ls /dev/input/js*`
- Test with `jstest /dev/input/js0`
- Install joystick utilities: `sudo apt-get install joystick`

### Robot not responding to commands
- Verify deadman switch (enable button) is held
- Check that robot is not in error state
- Ensure emergency stop is not activated
- Verify control mode matches robot capabilities

### Lag or delayed response
- Use wired Ethernet connection instead of WiFi
- Reduce update_rate in configuration
- Close other network-intensive applications
- Check robot CPU load

## 📚 API Documentation

See [docs/API.md](docs/API.md) for detailed API documentation.

### Core Classes

- `RobotController`: Main interface to RealMan robot
- `KeyboardTeleop`: Keyboard-based teleoperation
- `JoystickTeleop`: Joystick/gamepad teleoperation
- `JointControl`: Joint space control mode
- `CartesianControl`: Cartesian space control mode
- `VelocityControl`: Continuous velocity control mode
- `SafetyMonitor`: Safety feature management

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

### Development Setup
```bash
# Clone with development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run linter
pylint realman_teleop/

# Format code
black realman_teleop/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- RealMan Robotics for the RM_API2 library
- The robotics community for teleoperation best practices
- Contributors and testers

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/realman-teleop/issues)
- **Documentation**: [Full Documentation](https://github.com/yourusername/realman-teleop/wiki)
- **RealMan Support**: sales@realman-robot.com
- **RealMan Academy**: https://blog.csdn.net/realman_Rop

## 🗺️ Roadmap

- [ ] ROS/ROS2 integration
- [ ] Web-based control interface
- [ ] Mobile app control
- [ ] VR/AR teleoperation
- [ ] Multi-robot coordination
- [ ] Advanced path planning integration
- [ ] Vision-based teleoperation
- [ ] Haptic feedback support

## 📊 Status

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Coverage](https://img.shields.io/badge/coverage-85%25-yellow)

---

**Note**: This is a third-party library and is not officially affiliated with RealMan Robotics. Always refer to the official RealMan documentation for the most accurate and up-to-date information about your specific robot model.
# realman-teleop
