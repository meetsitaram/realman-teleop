# Safe Start Guide - Monitor First! 🛡️

## The Recommended Workflow

Before sending any commands to your robot, **monitor its state first**. This gives you confidence that:
- ✅ Connection is working
- ✅ Robot is responding
- ✅ You can read current joint positions
- ✅ Everything is ready for teleoperation

## 📊 Step 1: Monitor Robot (READ-ONLY)

### What is Monitor Mode?

The monitor script:
- ✅ **Only READS** robot state
- ✅ **Never SENDS** any commands
- ✅ Shows real-time joint angles, pose, and velocities
- ✅ Safe to run anytime
- ✅ Great for debugging connection issues

### Start Monitoring

```bash
conda activate realman-teleop
./teleop monitor
```

### What You'll See

**With Rich UI (if available):**
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                  🤖 Robot State Monitor                   ┃
┣━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ Property            ┃ Value                              ┃
┣━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ Robot Model         ┃ R1D2                               ┃
┃ IP Address          ┃ 192.168.1.18:8080                  ┃
┃ DOF                 ┃ 6                                  ┃
┃ Status              ┃ 🟡 Idle                            ┃
┣━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ Joint 1             ┃     0.00°                          ┃
┃ Joint 2             ┃    20.00°                          ┃
┃ Joint 3             ┃    70.00°                          ┃
┃ Joint 4             ┃     0.00°                          ┃
┃ Joint 5             ┃    90.00°                          ┃
┃ Joint 6             ┃     0.00°                          ┃
┣━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ Position X          ┃   0.3000 m                         ┃
┃ Position Y          ┃   0.0000 m                         ┃
┃ Position Z          ┃   0.4500 m                         ┃
┃ Rotation RX         ┃   3.1416 rad                       ┃
┃ Rotation RY         ┃   0.0000 rad                       ┃
┃ Rotation RZ         ┃   0.0000 rad                       ┃
┗━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

Press Ctrl+C to stop monitoring
This is READ-ONLY mode - no commands are sent to the robot
```

**Simple Mode (always works):**
```
================================================================================
Robot State Monitor - 2026-01-14 18:45:23
================================================================================

Status: 🟡 Idle

--- Joint Angles (degrees) ---
  Joint 1:     0.00° 
  Joint 2:    20.00° ██
  Joint 3:    70.00° ███████
  Joint 4:     0.00° 
  Joint 5:    90.00° █████████
  Joint 6:     0.00° 

--- End-Effector Pose ---
  Position: X= 0.3000m  Y= 0.0000m  Z= 0.4500m
  Rotation: RX= 3.1416rad RY= 0.0000rad RZ= 0.0000rad

--- Joint Velocities (deg/s) ---
  Joint 1:     0.00°/s
  Joint 2:     0.00°/s
  Joint 3:     0.00°/s
  Joint 4:     0.00°/s
  Joint 5:     0.00°/s
  Joint 6:     0.00°/s

================================================================================
Press Ctrl+C to stop monitoring
================================================================================
```

### Monitor Options

```bash
# Default monitor (10 Hz update)
./teleop monitor

# Faster updates (useful for watching motion)
./teleop monitor --rate 20

# Simple text mode (no rich UI)
./teleop monitor --simple

# With detailed logging
./teleop monitor --log INFO
```

### What to Check

While monitoring, verify:

1. **Joint Angles Look Reasonable**
   - All values within expected range (-180° to +180°)
   - Match what you see on the physical robot

2. **Values Update**
   - If you manually move robot (teach pendant), numbers should change
   - Confirms real-time communication

3. **No Errors**
   - Status should show "Idle" or "Moving" (if robot is moving)
   - No connection errors or timeouts

4. **Velocities are Zero When Idle**
   - All velocities should be near 0 when robot is not moving
   - If showing large velocities when idle, something is wrong

## 🎯 Step 2: Once Confident - Start Teleoperation

After successfully monitoring and verifying connection:

```bash
# Stop monitoring (Ctrl+C)

# Start keyboard teleoperation
./teleop keyboard
```

**Remember:** You can always go back to monitor mode anytime!

## 🛡️ When to Use Monitor Mode

### ✅ Use Monitor Mode When:

- First time connecting to a robot
- After changing network/IP settings
- Debugging connection issues
- Verifying robot is responding correctly
- Learning robot's coordinate system
- Checking if someone else is controlling robot
- After robot errors or reboots

### 🎮 Use Teleoperation When:

- You've successfully monitored the robot
- Connection is stable and reliable
- You understand the current robot pose
- Workspace is clear and safe

## 🐛 Troubleshooting with Monitor

### "Failed to connect to robot"

```bash
# Check network
ping 192.168.1.18

# Verify IP in config
cat .env

# Reconfigure
python setup_robot.py
```

### "No data available" for all fields

- Robot might be in error state - check teach pendant
- Emergency stop might be engaged
- Robot controller might need restart

### Values are frozen/not updating

- Network latency issues - check ping times
- Robot might be busy with another command
- Try lowering update rate: `./teleop monitor --rate 5`

### Connection works but values look wrong

- Different coordinate system? Check robot manual
- Wrong robot model configured? Run `./teleop setup`

## 💡 Pro Tips

1. **Always monitor first** - Make it a habit before teleoperation

2. **Leave monitor running** - Open in separate terminal while developing

3. **Use for debugging** - If teleoperation acts strange, check monitor

4. **Verify poses** - Before dangerous moves, check current pose in monitor

5. **Network quality check** - Update rate shows connection quality
   - 10 Hz updating smoothly = Good
   - Stuttering/freezing = Network issues

## 📝 Monitoring Checklist

Before teleoperation:

- [ ] Monitor connects successfully
- [ ] Joint angles display correctly
- [ ] Values update in real-time
- [ ] Robot status shows "Idle"
- [ ] Pose matches physical robot position
- [ ] Velocities are near zero when idle
- [ ] No error messages in output

**Once all checked ✅ → Ready for teleoperation!**

## 🔄 Comparison: Monitor vs Test vs Teleoperation

| Mode | Reads State | Sends Commands | Use Case |
|------|------------|----------------|----------|
| **Monitor** | ✅ Continuous | ❌ Never | Verify connection, watch state |
| **Test** | ✅ Once | ✅ Home position | Quick connection test |
| **Teleoperation** | ✅ Continuous | ✅ User control | Actual robot control |

**Recommendation:** Monitor → Test → Teleoperation

## 🚀 Complete Safe Start Sequence

```bash
# 1. Setup (once)
python setup_robot.py

# 2. Monitor (always first!)
./teleop monitor
# Watch for 30 seconds, verify connection

# 3. Test (optional - sends home command)
# Press Ctrl+C to stop monitor, then:
./teleop test

# 4. Teleoperation (once confident)
./teleop keyboard

# Tips:
# - Keep monitor running in separate terminal
# - Return to monitor if anything seems wrong
# - Monitor is your "robot dashboard"
```

## 🎓 Learning Exercise

Try this to understand your robot:

```bash
# Terminal 1: Start monitor
./teleop monitor

# Terminal 2: Manually move robot
# (Use teach pendant to move each joint)

# Observe in Terminal 1:
# - Joint angles change in real-time
# - End-effector position updates
# - Velocities spike during movement
```

This builds intuition about your robot's kinematics!

---

**Remember: When in doubt, monitor first! 📊🛡️**

It's the safest way to verify everything before sending commands.

