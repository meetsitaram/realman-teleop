# Setup Complete! 🎉

Your RealMan R1D2 teleoperation environment is now ready!

## What I've Done

### ✅ Added R1D2 Support

1. **Updated Robot Controller** (`realman_teleop/robot_controller.py`)
   - Added R1D2 to the list of supported models
   - Configured as a 6-DOF single arm robot
   - Using RM65 base configuration (6 joints)
   - Default home position: `[0, 20, 70, 0, 90, 0]` degrees

2. **Updated Configuration Files**
   - `config/robot_config.example.yaml` - Now lists R1D2 as supported model
   - Both keyboard and joystick examples now accept R1D2 as a model option

3. **Updated Documentation**
   - `README.md` - Added R1D2 to supported models
   - Created `R1D2_QUICKSTART.md` - Complete guide specific to R1D2

### ✅ Created Conda Environment Setup

1. **Created `environment.yml`**
   - Python 3.10 environment
   - All required dependencies (numpy, pygame, PyYAML, etc.)
   - RealMan Robotic_Arm API
   - Development tools (ipython, jupyter)

2. **Created `install.sh`**
   - Automated installation script
   - Creates conda environment
   - Installs all dependencies
   - Copies configuration files
   - Provides helpful next steps

3. **Created `verify_setup.py`**
   - Verification script to check installation
   - Tests all dependencies
   - Checks project structure
   - Confirms configuration files

## Next Steps - Quick Start

### 1. Run Installation (5 minutes)

```bash
# Navigate to project directory
cd /home/sitaram/projects/realman-teleop

# Run the installation script
./install.sh
```

This will:
- Create a conda environment named `realman-teleop`
- Install all Python dependencies
- Set up configuration files

### 2. Activate Environment

```bash
conda activate realman-teleop
```

### 3. Verify Installation

```bash
python verify_setup.py
```

This checks that everything is installed correctly.

### 4. Configure Your R1D2

Edit the robot configuration file:

```bash
nano config/robot_config.yaml
```

Change these lines:

```yaml
robot:
  ip: "192.168.1.18"  # ← YOUR R1D2'S IP ADDRESS
  port: 8080
  model: "R1D2"       # ← Change from RM65 to R1D2
```

### 5. Test Connection

Make sure your R1D2 is:
- ✅ Powered on
- ✅ Connected to the same network
- ✅ Reachable (test with: `ping YOUR_ROBOT_IP`)

Then test the connection:

```bash
python examples/basic_usage.py
```

### 6. Start Teleoperation! 🤖

#### Option A: Keyboard Control

```bash
python examples/keyboard_teleop.py --model R1D2
```

Or specify IP directly:

```bash
python examples/keyboard_teleop.py --ip 192.168.1.18 --model R1D2
```

**Keyboard Controls:**
- `W/S/A/D/Q/E` - Move robot (forward/back, left/right, up/down)
- `I/K/J/L/U/O` - Rotate robot
- **`SHIFT` - HOLD to enable** (deadman switch) ⚠️
- `SPACE` - Emergency stop
- `TAB` - Switch mode
- `H` - Go home

#### Option B: Joystick Control

First, connect your USB gamepad, then:

```bash
# List available joysticks
python examples/list_joysticks.py

# Start joystick control
python examples/joystick_teleop.py --model R1D2
```

**Joystick Controls:**
- Left Stick - Move left/right, forward/backward
- Right Stick - Rotate and vertical
- **`LB/L1` - HOLD to enable** (deadman switch) ⚠️
- `RB/R1` - Turbo speed
- `Back/Select` - Emergency stop

## Safety Reminders ⚠️

Before moving the robot:

1. ✅ **Clear the workspace** - Remove obstacles and people
2. ✅ **Know your emergency stop** - SPACE or Back button
3. ✅ **Use deadman switch** - Hold SHIFT or LB to move
4. ✅ **Start slow** - Begin with 0.1 m/s speed
5. ✅ **Test safely** - First movements in known safe area

## Project Files Created/Modified

### New Files Created:
- ✨ `environment.yml` - Conda environment specification
- ✨ `install.sh` - Automated installation script
- ✨ `verify_setup.py` - Setup verification script
- ✨ `R1D2_QUICKSTART.md` - R1D2-specific quick start guide
- ✨ `SETUP_COMPLETE.md` - This file!

### Files Modified:
- 📝 `realman_teleop/robot_controller.py` - Added R1D2 support
- 📝 `config/robot_config.example.yaml` - Added R1D2 to model list
- 📝 `examples/keyboard_teleop.py` - Added R1D2 to choices
- 📝 `examples/joystick_teleop.py` - Added R1D2 to choices
- 📝 `README.md` - Added R1D2 to supported models

## Useful Commands

```bash
# Activate environment
conda activate realman-teleop

# Verify setup
python verify_setup.py

# Test connection
python examples/basic_usage.py

# Keyboard teleoperation with custom IP
python examples/keyboard_teleop.py --ip 192.168.1.18 --model R1D2 --speed 0.1

# Joystick teleoperation
python examples/joystick_teleop.py --model R1D2

# List joysticks
python examples/list_joysticks.py

# Deactivate environment
conda deactivate
```

## Configuration Tips

### Adjust Movement Speeds

Edit `config/robot_config.yaml`:

```yaml
limits:
  max_linear_velocity: 0.5    # meters/second (0.1-1.0 recommended)
  max_angular_velocity: 1.0   # radians/second
  max_joint_velocity: 30.0    # degrees/second
```

### Set Workspace Limits (Safety Boundaries)

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

### Customize Key Mappings

Edit `config/keyboard_config.yaml` or `config/joystick_config.yaml`.

## Troubleshooting

### Connection Issues

```bash
# Test network connectivity
ping 192.168.1.18

# Check firewall
sudo ufw status

# Verify robot is on and connected
```

### Robot Not Moving

- **Holding deadman switch?** (SHIFT or LB)
- **Emergency stop activated?** Press `H` to go home
- **Speed set to zero?** Check config file
- **Robot in error state?** Check status lights

### Permission Errors (Keyboard)

```bash
# Option 1: Run with sudo (not recommended)
sudo python examples/keyboard_teleop.py --model R1D2

# Option 2: Add user to input group (recommended)
sudo usermod -a -G input $USER
# Then logout and login
```

### Joystick Not Detected

```bash
# Install joystick utilities
sudo apt-get install joystick jstest-gtk

# List joystick devices
ls /dev/input/js*

# Test joystick
jstest /dev/input/js0
```

## Documentation

- 📖 `START_HERE.md` - General project quick start
- 📖 `R1D2_QUICKSTART.md` - R1D2-specific guide
- 📖 `docs/QUICKSTART.md` - Detailed setup guide
- 📖 `docs/API.md` - Complete API reference
- 📖 `docs/TROUBLESHOOTING.md` - Common issues and solutions
- 📖 `PROJECT_SUMMARY.md` - Complete project overview

## Python API Example

You can also control the robot programmatically:

```python
from realman_teleop import RobotController

# Connect to R1D2
with RobotController(ip="192.168.1.18", model="R1D2") as robot:
    # Move to home position
    robot.move_to_home()
    
    # Move joints (degrees)
    robot.movej([0, 30, 60, 0, 90, 0], velocity=20)
    
    # Move in Cartesian space (meters, radians)
    robot.movel([0.3, 0, 0.3, 3.14, 0, 0], velocity=20)
    
    # Get current state
    pose = robot.get_current_pose()
    joints = robot.get_current_joint_angles()
```

## Support & Resources

- **RealMan Official Support**: sales@realman-robot.com
- **RealMan Documentation**: https://develop.realman-robotics.com/
- **Project Documentation**: See `docs/` folder

## Notes on R1D2 Configuration

The R1D2 model has been configured using the RM65 base settings:
- 6 degrees of freedom (6-DOF)
- Default home position: `[0, 20, 70, 0, 90, 0]` degrees
- Using standard RM65 model enum

If you experience issues or need to adjust these settings:
1. Check your R1D2 manual for specific joint limits
2. Modify the home position in `realman_teleop/robot_controller.py` if needed
3. Adjust velocity limits in `config/robot_config.yaml`

## Summary

✅ **R1D2 support added** to the teleoperation library  
✅ **Conda environment** configured with all dependencies  
✅ **Installation script** created for easy setup  
✅ **Verification script** to check installation  
✅ **Documentation** updated with R1D2 information  

You're all set! 🚀 Run `./install.sh` to begin!

---

**Happy teleoperating! 🤖**

*Remember: Safety first - always use the deadman switch and keep emergency stop ready!*

