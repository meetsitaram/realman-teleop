# Easy Setup Guide - No More IP Hassles! 🎉

This simplified setup means you only configure your robot **once**, then use simple commands forever!

## 🚀 One-Time Setup (5 minutes)

### Step 1: Install Everything

```bash
cd /home/sitaram/projects/realman-teleop
./install.sh
```

### Step 2: Activate Environment

```bash
conda activate realman-teleop
```

### Step 3: Configure Your Robot (Interactive)

```bash
python setup_robot.py
```

This wizard will ask you:
- Robot IP address (with automatic ping test)
- Robot model (RM65, RM75, ECO65, GEN72, **R1D2**, etc.)
- Port (default: 8080)
- Default speed
- Log level

**Your settings are saved to `.env` file and automatically used by all commands!**

---

## 🎮 Daily Use - Super Simple!

After the one-time setup, you never need to pass IP or model again!

### Test Connection

```bash
./teleop test
```

### Keyboard Teleoperation

```bash
./teleop keyboard
```

### Joystick Teleoperation

```bash
# First time: check which device
./teleop list

# Then start
./teleop joystick
```

### Other Commands

```bash
./teleop setup      # Reconfigure robot settings
./teleop verify     # Verify installation
./teleop --help     # Show all commands
```

---

## 📝 What Got Configured?

After running `setup_robot.py`, you have a `.env` file that looks like:

```bash
# Robot Connection Settings
ROBOT_IP=192.168.1.18      # Your robot's IP
ROBOT_PORT=8080
ROBOT_MODEL=R1D2           # Your robot model

# Control Settings
DEFAULT_SPEED=0.1
DEFAULT_UPDATE_RATE=100

# Logging
LOG_LEVEL=INFO
```

**All scripts automatically read from this file!**

---

## 🔧 Change Settings Later

### Option 1: Run Setup Wizard Again

```bash
python setup_robot.py
```

### Option 2: Edit .env Directly

```bash
nano .env
```

Change your robot's IP, model, or any setting. All scripts will use the new values immediately!

---

## 🆚 Old Way vs New Way

### ❌ Old Way (tedious):

```bash
python examples/keyboard_teleop.py --ip 192.168.1.18 --model R1D2 --speed 0.1 --rate 100
python examples/joystick_teleop.py --ip 192.168.1.18 --model R1D2
python examples/basic_usage.py --ip 192.168.1.18 --model R1D2
```

### ✅ New Way (simple):

```bash
./teleop keyboard
./teleop joystick
./teleop test
```

**All settings loaded automatically from `.env`!**

---

## 🎯 Quick Command Reference

| Command | What It Does |
|---------|--------------|
| `./teleop keyboard` | Start keyboard control |
| `./teleop joystick` | Start joystick control |
| `./teleop test` | Test robot connection |
| `./teleop list` | List joystick devices |
| `./teleop setup` | Configure/reconfigure robot |
| `./teleop verify` | Verify installation |

### With Options

```bash
# Override speed temporarily
./teleop keyboard --speed 0.2

# Change log level
./teleop keyboard --log DEBUG

# Still works! Options override .env settings
./teleop keyboard --speed 0.05 --log WARNING
```

---

## 🔍 Behind the Scenes

### Configuration Priority (highest to lowest):

1. **Command-line arguments** - `--ip`, `--model`, etc.
2. **Environment variables** - `.env` file
3. **YAML config** - `config/robot_config.yaml`
4. **Defaults** - Built-in defaults

So you can:
- Set defaults in `.env` (most common case)
- Override temporarily with command-line args when needed
- Everything "just works"!

---

## 📂 Files Created

After setup, you'll have:

```
realman-teleop/
├── .env                    # Your robot config (auto-loaded)
├── env.template            # Template for .env
├── setup_robot.py          # Setup wizard
├── teleop                  # Quick command wrapper
├── config/
│   ├── robot_config.yaml   # YAML config (optional)
│   ├── keyboard_config.yaml
│   └── joystick_config.yaml
└── ...
```

---

## 🛡️ Safety Note

The `.env` file contains your robot's network configuration. You can:
- Keep it private (it's in `.gitignore`)
- Change it anytime with `python setup_robot.py`
- Edit it directly with any text editor

---

## 🐛 Troubleshooting

### "Configuration file (.env) not found"

```bash
# Run setup
python setup_robot.py

# Or manually copy template
cp env.template .env
nano .env  # Edit your robot's IP
```

### "Cannot connect to robot"

```bash
# Test network
ping YOUR_ROBOT_IP

# Reconfigure
python setup_robot.py

# Or edit .env directly
nano .env
```

### "Conda environment not activated"

```bash
conda activate realman-teleop
```

The `./teleop` script will try to auto-activate if needed!

---

## 🎓 Advanced: Multiple Robots

Got multiple robots? Easy!

### Option 1: Multiple .env Files

```bash
# Save different configs
cp .env .env.robot1
cp .env .env.robot2

# Switch between them
cp .env.robot1 .env  # Use robot 1
./teleop keyboard

cp .env.robot2 .env  # Use robot 2
./teleop keyboard
```

### Option 2: Command-line Override

```bash
# Use .env defaults most of the time
./teleop keyboard

# Override for different robot
python examples/keyboard_teleop.py --ip 192.168.1.20 --model RM65
```

---

## 💡 Pro Tips

1. **One setup per robot** - If you move to a different robot, just run `python setup_robot.py` again

2. **Quick testing** - The setup wizard pings your robot to verify connectivity

3. **Version control** - `.env` is in `.gitignore`, so your robot IP stays private

4. **Team sharing** - Share `env.template` with teammates, they fill in their robot's IP

5. **Documentation** - Your `.env` file is self-documenting with comments!

---

## ✨ Summary

**Before:**
- Pass `--ip` and `--model` to every command
- Remember robot's IP every time
- Long, repetitive commands

**After:**
- Configure once with `setup_robot.py`
- Simple commands: `./teleop keyboard`
- Settings automatically loaded
- Override when needed

**Setup time:** 5 minutes  
**Time saved:** Forever! ⏰✨

---

**Happy teleoperating with fewer keystrokes! 🤖**

