# 🚀 RealMan Robot Teleoperation - START HERE!

Thank you for downloading this project! Here's how to get started immediately.

## ⚡ Quickest Start (5 minutes)

```bash
# 1. Install dependencies
pip install Robotic_Arm numpy PyYAML pygame

# 2. Configure your robot (edit with your IP)
cp config/robot_config.example.yaml config/robot_config.yaml
nano config/robot_config.yaml  # Change IP to your robot's IP

# 3. Test connection
python examples/basic_usage.py

# 4. Start keyboard control
python examples/keyboard_teleop.py
```

## 📁 What's in This Project?

### Main Code (`realman_teleop/`)
- **robot_controller.py** - Connect and control your robot
- **keyboard_teleop.py** - Control with keyboard (WASD + IJKL)
- **joystick_teleop.py** - Control with gamepad/joystick
- **safety.py** - Safety features (limits, deadman switch, e-stop)
- **control_modes.py** - Joint/Cartesian/Velocity control modes
- Plus utility modules for configuration and helpers

### Examples (`examples/`)
- **basic_usage.py** - Simple API usage example
- **keyboard_teleop.py** - Full keyboard control
- **joystick_teleop.py** - Full joystick control
- **list_joysticks.py** - Find your joystick device

### Configuration (`config/`)
- **robot_config.example.yaml** - Robot connection settings
- **joystick_config.example.yaml** - Joystick button mapping
- **keyboard_config.example.yaml** - Keyboard key mapping

### Documentation (`docs/`)
- **QUICKSTART.md** - Detailed getting started guide
- **API.md** - Complete API reference
- **TROUBLESHOOTING.md** - Common issues and solutions

## 🎯 Choose Your Control Method

### Option 1: Keyboard Control (Easiest)

```bash
python examples/keyboard_teleop.py --ip 192.168.1.18 --model RM65
```

**Controls:**
- **WASD + QE**: Move robot
- **IJKLUO**: Rotate robot
- **Hold SHIFT**: Enable motion (deadman switch)
- **SPACE**: Emergency stop
- **TAB**: Switch between Cartesian/Joint mode
- **H**: Go home

### Option 2: Joystick Control (Best for smooth control)

```bash
# First, find your joystick
python examples/list_joysticks.py

# Then start control
python examples/joystick_teleop.py --device 0
```

**Controls:**
- **Left Stick**: Move left/right, forward/backward
- **Right Stick**: Rotate and move up/down
- **Hold LB/L1**: Enable motion (deadman switch)
- **RB/R1**: Turbo speed
- **Back/Select**: Emergency stop
- **Start**: Switch mode
- **B/Circle**: Go home

## ⚙️ Configuration

Edit `config/robot_config.yaml`:

```yaml
robot:
  ip: "192.168.1.18"  # ← Change this to your robot's IP
  port: 8080
  model: "RM65"       # ← Change to your model (RM65/RM75/RML63/ECO65/GEN72)

speeds:
  linear: 0.1    # m/s - Adjust as needed
  angular: 0.3   # rad/s
```

## 🛡️ Safety First!

**Before moving the robot:**
1. ✅ Clear the workspace
2. ✅ Know where emergency stop is (SPACE or Back button)
3. ✅ Start with low speeds
4. ✅ Always hold deadman switch (SHIFT or LB)
5. ✅ Test in safe area first

## 📚 Next Steps

1. **Read Documentation**
   - `docs/QUICKSTART.md` - Detailed setup guide
   - `docs/API.md` - Full API reference
   - `docs/TROUBLESHOOTING.md` - Fix common issues

2. **Customize**
   - Edit configuration files for your needs
   - Adjust button/key mappings
   - Change speed limits
   - Set workspace boundaries

3. **Extend**
   - Write custom control scripts using the API
   - Add new control modes
   - Integrate with your application

## 🐛 Common Issues

### "Cannot connect to robot"
```bash
# Check robot is on same network
ping 192.168.1.18

# Verify IP in config file
cat config/robot_config.yaml
```

### "No joysticks found"
```bash
# List available joysticks
python examples/list_joysticks.py

# Check USB connection
ls /dev/input/js*  # Linux
```

### "Robot not moving"
- Are you holding the deadman switch? (SHIFT or LB)
- Check robot isn't in error state
- Verify speeds aren't set to 0

**More help**: See `docs/TROUBLESHOOTING.md`

## 🔧 Python API Usage

```python
from realman_teleop import RobotController

# Connect to robot
with RobotController(ip="192.168.1.18", model="RM65") as robot:
    # Move to home position
    robot.move_to_home()
    
    # Move joints
    robot.movej([0, 30, 60, 0, 90, 0], velocity=20)
    
    # Move in Cartesian space
    robot.movel([0.3, 0, 0.3, 3.14, 0, 0], velocity=20)
    
    # Get current state
    pose = robot.get_current_pose()
    joints = robot.get_current_joint_angles()
```

## 📦 Full Installation (Recommended)

```bash
# Clone or download project
cd realman-teleop

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt

# Install RealMan API
pip install Robotic_Arm

# Copy configuration files
cp config/robot_config.example.yaml config/robot_config.yaml
cp config/joystick_config.example.yaml config/joystick_config.yaml
cp config/keyboard_config.example.yaml config/keyboard_config.yaml

# Edit robot IP address
nano config/robot_config.yaml
```

## 🤝 Support

- **Documentation**: Check `docs/` folder
- **Issues**: Open GitHub issue (if repository available)
- **RealMan Official**: sales@realman-robot.com
- **RealMan Docs**: https://develop.realman-robotics.com/

## 📊 Project Features

✅ Full keyboard control
✅ Full joystick/gamepad control
✅ Joint space control
✅ Cartesian space control
✅ Velocity control
✅ Safety monitoring (deadman, e-stop, limits)
✅ Collision detection integration
✅ Configurable via YAML
✅ Supports all RealMan models
✅ Well-documented API
✅ Production-ready code
✅ Example scripts included

## 🎓 Learn More

- **PROJECT_SUMMARY.md** - Complete project overview
- **README.md** - Comprehensive documentation
- **docs/API.md** - API reference
- **docs/QUICKSTART.md** - Detailed setup
- **docs/TROUBLESHOOTING.md** - Problem solving

## 🚀 You're Ready!

Your robot teleoperation system is ready to use. Configure your robot's IP address and start exploring!

**Have fun and stay safe! 🤖**

---

*This is a complete, production-ready skeleton for RealMan robot teleoperation. Customize it for your specific needs!*
