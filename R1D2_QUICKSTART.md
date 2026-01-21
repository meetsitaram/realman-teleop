# R1D2 Single Arm Robot - Quick Start Guide

This guide will help you set up and start teleoperating your R1D2 single arm robot.

## Prerequisites

- R1D2 robot powered on and connected to network
- Linux computer (Ubuntu 20.04+ recommended)
- Network connection between computer and robot

## Installation

### Step 1: Run the Installation Script

```bash
# Make the install script executable
chmod +x install.sh

# Run the installation script
./install.sh
```

This will:
- Create a conda environment named `realman-teleop`
- Install all required dependencies
- Copy configuration files

### Step 2: Activate the Environment

```bash
conda activate realman-teleop
```

### Step 3: Configure Your Robot

Edit the robot configuration file with your R1D2's IP address:

```bash
nano config/robot_config.yaml
```

Update the following fields:

```yaml
robot:
  ip: "192.168.1.18"  # ← Change to your R1D2's IP address
  port: 8080
  model: "R1D2"       # ← Set to R1D2
```

## Testing Connection

Before starting teleoperation, test the connection:

```bash
python examples/basic_usage.py
```

If successful, you should see:
- Connection confirmation
- Robot software information
- Current joint angles and pose

## Keyboard Teleoperation

Start keyboard control:

```bash
python examples/keyboard_teleop.py --model R1D2
```

Or with direct IP specification:

```bash
python examples/keyboard_teleop.py --ip 192.168.1.18 --model R1D2
```

### Keyboard Controls

**Movement (Cartesian Space):**
- `W` / `S`: Move forward / backward
- `A` / `D`: Move left / right
- `Q` / `E`: Move up / down

**Rotation:**
- `I` / `K`: Pitch (tilt forward/backward)
- `J` / `L`: Roll (tilt left/right)
- `U` / `O`: Yaw (rotate left/right)

**Control:**
- `SHIFT`: **HOLD to enable motion** (deadman switch) ⚠️
- `SPACE`: Emergency stop
- `TAB`: Switch control mode (Cartesian/Joint)
- `+` / `-`: Increase/decrease speed
- `H`: Move to home position

## Joystick Teleoperation

### Step 1: Connect Your Joystick

Connect a USB gamepad (Xbox, PS4, PS5, or generic USB controller).

### Step 2: Find Your Joystick Device

```bash
python examples/list_joysticks.py
```

This will show available joystick devices.

### Step 3: Start Joystick Control

```bash
python examples/joystick_teleop.py --model R1D2
```

Or with specific device:

```bash
python examples/joystick_teleop.py --model R1D2 --device 0
```

### Joystick Controls

**Left Stick:**
- Horizontal: Move left/right
- Vertical: Move forward/backward

**Right Stick:**
- Controls rotation and vertical movement

**Buttons:**
- `LB` / `L1`: **HOLD to enable motion** (deadman switch) ⚠️
- `RB` / `R1`: Hold for turbo speed
- `Back` / `Select`: Emergency stop
- `Start`: Switch control mode
- `B` / `Circle`: Move to home position

## Safety Guidelines

### ⚠️ IMPORTANT SAFETY RULES

1. **Clear the workspace** - Remove all obstacles and people from robot reach
2. **Know your emergency stop** - SPACE key or Back/Select button
3. **Use the deadman switch** - Robot only moves when held (SHIFT or LB)
4. **Start with low speeds** - Begin at 0.1 m/s, increase gradually
5. **Test in safe area** - First movements in known safe positions
6. **Stay alert** - Always be ready to release deadman switch

### Safety Features Built-In

- ✅ Deadman switch (must be held for robot to move)
- ✅ Emergency stop (immediate halt)
- ✅ Velocity limits (configurable)
- ✅ Workspace boundaries (configurable)
- ✅ Collision detection integration

## Configuration

### Adjusting Speeds

Edit `config/robot_config.yaml`:

```yaml
limits:
  max_linear_velocity: 0.5    # m/s (0.1-1.0 recommended)
  max_angular_velocity: 1.0   # rad/s
  max_joint_velocity: 30.0    # deg/s
```

### Setting Workspace Limits

To restrict robot movement to a safe area:

```yaml
limits:
  workspace:
    x_min: -0.5
    x_max: 0.5
    y_min: -0.5
    y_max: 0.5
    z_min: 0.1
    z_max: 0.8
```

### Customizing Button Mappings

Edit `config/keyboard_config.yaml` or `config/joystick_config.yaml` to remap buttons/keys to your preference.

## Troubleshooting

### Cannot Connect to Robot

```bash
# Check network connection
ping 192.168.1.18

# Verify robot is powered on and ethernet cable is connected
# Check that IP address in config is correct
cat config/robot_config.yaml
```

### Robot Not Moving

- **Are you holding the deadman switch?** (SHIFT or LB)
- **Is emergency stop activated?** Press `H` to go home and reset
- **Check robot status lights** - Should be green/ready
- **Verify speeds aren't set to 0** in config file

### Joystick Not Detected

```bash
# List USB devices
lsusb

# Check input devices
ls /dev/input/js*

# Install joystick utilities
sudo apt-get install joystick jstest-gtk

# Test joystick
jstest /dev/input/js0
```

### Permission Denied (Keyboard)

On Linux, keyboard control may require root:

```bash
# Run with sudo (not recommended for production)
sudo python examples/keyboard_teleop.py --model R1D2

# Or add user to input group
sudo usermod -a -G input $USER
# Then logout and login again
```

## Advanced Usage

### Python API

You can also control the R1D2 programmatically:

```python
from realman_teleop import RobotController

# Connect to robot
with RobotController(ip="192.168.1.18", model="R1D2") as robot:
    # Move to home
    robot.move_to_home()
    
    # Move joints (degrees)
    robot.movej([0, 30, 60, 0, 90, 0], velocity=20)
    
    # Move in Cartesian space (meters, radians)
    robot.movel([0.3, 0, 0.3, 3.14, 0, 0], velocity=20)
    
    # Get current state
    pose = robot.get_current_pose()
    joints = robot.get_current_joint_angles()
    
    print(f"Current pose: {pose}")
    print(f"Current joints: {joints}")
```

### Custom Control Scripts

See `examples/basic_usage.py` for a template to create your own control scripts.

## Next Steps

1. **Read Full Documentation**
   - `START_HERE.md` - General quick start
   - `docs/QUICKSTART.md` - Detailed setup guide
   - `docs/API.md` - Complete API reference
   - `docs/TROUBLESHOOTING.md` - Common issues

2. **Customize Configuration**
   - Adjust speed limits
   - Set workspace boundaries
   - Remap buttons/keys

3. **Develop Custom Applications**
   - Use the Python API
   - Integrate with your workflow
   - Add custom control modes

## Support

- **Documentation**: See `docs/` folder
- **RealMan Support**: sales@realman-robot.com
- **RealMan Documentation**: https://develop.realman-robotics.com/

## Notes

- The R1D2 model uses the RM65 base configuration as a starting point
- If you encounter issues specific to R1D2, you may need to adjust the default joint positions in `realman_teleop/robot_controller.py`
- Always refer to your R1D2 manual for model-specific information

---

**Happy teleoperating! 🤖**

*Remember: Safety first, always use the deadman switch, and keep emergency stop ready!*

