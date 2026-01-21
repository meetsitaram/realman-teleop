# Quick Start Guide

Get up and running with RealMan robot teleoperation in minutes!

## Prerequisites

- RealMan robotic arm (any supported model)
- Python 3.9 or higher
- Network connection to robot
- (Optional) USB gamepad/joystick

## Step 1: Installation

```bash
# Clone repository
git clone https://github.com/yourusername/realman-teleop.git
cd realman-teleop

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install RealMan API
pip install Robotic_Arm
```

## Step 2: Configuration

```bash
# Copy example configuration
cp config/robot_config.example.yaml config/robot_config.yaml

# Edit with your robot's IP address
nano config/robot_config.yaml
```

Change the IP address to match your robot:
```yaml
robot:
  ip: "192.168.1.18"  # Change to your robot's IP
  port: 8080
  model: "RM65"       # Change to your robot model
```

## Step 3: Test Connection

Run the basic usage example to verify connection:

```bash
python examples/basic_usage.py
```

If successful, you should see:
```
Connecting to robot...
Connected successfully!
Current Robot State...
```

## Step 4: Choose Control Method

### Option A: Keyboard Control

Best for quick testing and debugging.

```bash
python examples/keyboard_teleop.py
```

**Basic Controls:**
- Hold **SHIFT** to enable motion
- **W/A/S/D/Q/E** to move
- **I/J/K/L/U/O** to rotate
- **SPACE** for emergency stop

### Option B: Joystick Control

Best for smooth, intuitive control.

```bash
# First, list available joysticks
python examples/list_joysticks.py

# Then run teleoperation
python examples/joystick_teleop.py --device 0
```

**Basic Controls:**
- Hold **LB/L1** to enable motion
- **Left stick** to move
- **Right stick** to rotate
- **Back/Select** for emergency stop

## Step 5: Safety First!

⚠️ **Important Safety Tips:**

1. **Start with low speed**: Use default speeds first
2. **Enable deadman switch**: Always hold enable button
3. **Clear workspace**: Ensure robot has clear path
4. **Emergency stop**: Know where it is (SPACE or Back button)
5. **Test in simulation**: If available, test there first

## Common First-Time Issues

### "Cannot connect to robot"
- Check IP address matches robot
- Ensure robot is powered on
- Try: `ping 192.168.1.18`

### "No joysticks found"
- Plug in USB joystick
- Run: `python examples/list_joysticks.py`
- Check: `ls /dev/input/js*` (Linux)

### "Robot not responding"
- Hold enable button (SHIFT or LB)
- Check robot not in error state
- Try clearing errors: `robot.clear_errors()`

## Next Steps

### Adjust Settings

Edit `config/robot_config.yaml` to customize:
- Movement speeds
- Safety limits
- Workspace boundaries
- Update rate

### Try Other Examples

```bash
# Cartesian control
python examples/cartesian_control.py

# Joint control
python examples/joint_control.py

# Custom mapping
python examples/custom_mapping.py
```

### Read Documentation

- [Full API Documentation](docs/API.md)
- [Configuration Guide](docs/CONFIGURATION.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

## Getting Help

- **Issues**: Open GitHub issue
- **Questions**: Check documentation
- **RealMan Support**: sales@realman-robot.com

## What's Next?

Once you're comfortable with basic teleoperation:

1. **Customize controls**: Edit configuration files
2. **Write scripts**: Use Python API directly
3. **Add features**: Extend the library
4. **Integrate**: Add to your application

Example custom script:
```python
from realman_teleop import RobotController

with RobotController(ip="192.168.1.18", model="RM65") as robot:
    # Your custom code here
    robot.move_to_home()
    robot.movej([0, 30, 60, 0, 90, 0], velocity=20)
```

Happy robot controlling! 🤖
