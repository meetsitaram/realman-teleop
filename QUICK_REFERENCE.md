# Quick Reference Card - R1D2 Teleoperation

## 🚀 First Time Setup (5 minutes)

```bash
# 1. Run installation
./install.sh

# 2. Activate environment
conda activate realman-teleop

# 3. Configure robot (interactive)
python setup_robot.py

# 4. Monitor robot state (READ-ONLY, safe!)
./teleop monitor

# 5. Once confident, start teleoperation
./teleop keyboard
```

## ⌨️ Keyboard Control

### Start
```bash
conda activate realman-teleop
python examples/keyboard_teleop.py --model R1D2 --ip 192.168.1.18
```

### Controls
| Key | Action |
|-----|--------|
| **SHIFT** | **HOLD to enable motion** ⚠️ |
| W / S | Forward / Backward |
| A / D | Left / Right |
| Q / E | Up / Down |
| I / K | Pitch (tilt forward/back) |
| J / L | Roll (tilt left/right) |
| U / O | Yaw (rotate) |
| **SPACE** | **Emergency Stop** |
| TAB | Switch mode |
| H | Go home |
| + / - | Speed up/down |

## 🎮 Joystick Control

### Start
```bash
conda activate realman-teleop
python examples/list_joysticks.py  # Find device
python examples/joystick_teleop.py --model R1D2 --ip 192.168.1.18
```

### Controls
| Button/Stick | Action |
|--------------|--------|
| **LB / L1** | **HOLD to enable motion** ⚠️ |
| Left Stick | Move horizontal/forward-back |
| Right Stick | Rotate & vertical |
| RB / R1 | Turbo mode |
| **Back / Select** | **Emergency Stop** |
| Start | Switch mode |
| B / Circle | Go home |

## 🛡️ Safety Checklist

- [ ] Workspace is clear
- [ ] Emergency stop is ready (SPACE or Back button)
- [ ] Starting with low speed (0.1 m/s)
- [ ] Holding deadman switch to move (SHIFT or LB)
- [ ] First test in safe position

## 🔧 Common Commands

```bash
# Activate environment
conda activate realman-teleop

# Monitor robot (READ-ONLY - safest first step!)
./teleop monitor

# Test connection
./teleop test

# Keyboard teleoperation
./teleop keyboard

# Joystick teleoperation  
./teleop joystick

# List joysticks
./teleop list

# Verify setup
./teleop verify

# Setup/reconfigure
./teleop setup
```

## ⚙️ Quick Configuration

### Change Speed Limits
Edit `config/robot_config.yaml`:
```yaml
limits:
  max_linear_velocity: 0.5    # m/s
  max_angular_velocity: 1.0   # rad/s
```

### Set Workspace Boundaries
```yaml
limits:
  workspace:
    x_min: -0.5
    x_max: 0.5
    z_min: 0.1
    z_max: 0.8
```

## 🐛 Quick Troubleshooting

**Robot not connecting?**
```bash
ping 192.168.1.18  # Test network
cat config/robot_config.yaml  # Check IP
```

**Robot not moving?**
- Are you holding SHIFT or LB? (deadman switch)
- Is emergency stop activated? Press H to reset
- Check robot status lights

**Joystick not detected?**
```bash
ls /dev/input/js*  # List devices
sudo apt-get install joystick  # Install tools
jstest /dev/input/js0  # Test joystick
```

**Permission denied (keyboard)?**
```bash
sudo usermod -a -G input $USER  # Add to input group
# Then logout and login
```

## 📚 Documentation

- `SETUP_COMPLETE.md` - Full setup guide
- `R1D2_QUICKSTART.md` - R1D2-specific guide
- `START_HERE.md` - Project overview
- `docs/TROUBLESHOOTING.md` - Detailed troubleshooting

## 🔑 Python API Quick Example

```python
from realman_teleop import RobotController

# Connect and control
with RobotController(ip="192.168.1.18", model="R1D2") as robot:
    robot.move_to_home()
    robot.movej([0, 30, 60, 0, 90, 0], velocity=20)
    pose = robot.get_current_pose()
    print(f"Current pose: {pose}")
```

---

**⚠️ Always hold deadman switch (SHIFT/LB) and keep emergency stop ready!**

