# Troubleshooting Guide

## Connection Issues

### Cannot connect to robot

**Symptoms**: Connection fails, timeout errors

**Solutions**:
1. Verify robot IP address
   ```bash
   ping 192.168.1.18
   ```

2. Check network connection
   - Ensure robot and computer are on same network
   - Try direct Ethernet connection
   - Check firewall settings

3. Verify robot is powered on and initialized
   - Check robot status LEDs
   - Verify robot controller is running

4. Check port availability
   ```bash
   # Linux/Mac
   netstat -an | grep 8080
   
   # Windows
   netstat -an | findstr 8080
   ```

5. Try different port or IP
   ```python
   robot = RobotController(ip="192.168.1.18", port=8080)
   ```

### Connection drops during operation

**Solutions**:
1. Use wired Ethernet instead of WiFi
2. Check network quality
3. Reduce update rate in configuration
4. Check for network congestion

## Input Device Issues

### Joystick not detected

**Symptoms**: "No joysticks found" error

**Solutions**:
1. Check USB connection
2. List available devices:
   ```bash
   # Linux
   ls /dev/input/js*
   
   # Or use the utility
   python examples/list_joysticks.py
   ```

3. Install joystick utilities (Linux):
   ```bash
   sudo apt-get install joystick
   jstest /dev/input/js0
   ```

4. Check permissions (Linux):
   ```bash
   sudo chmod 666 /dev/input/js0
   ```

5. Try different USB port

### Keyboard input not working

**Solutions**:
1. Ensure pygame window has focus
2. Click on pygame window
3. Check if other applications are capturing input
4. Try running with sudo (Linux only):
   ```bash
   sudo python examples/keyboard_teleop.py
   ```

### Joystick buttons/axes wrong

**Solutions**:
1. Test joystick with jstest:
   ```bash
   jstest /dev/input/js0
   ```

2. Update joystick configuration file
3. Use different button/axis mapping
4. Recalibrate joystick:
   ```bash
   jscal /dev/input/js0
   ```

## Robot Control Issues

### Robot not responding to commands

**Symptoms**: Commands sent but robot doesn't move

**Solutions**:
1. Check deadman switch is held
   - Keyboard: Hold SHIFT
   - Joystick: Hold LB/L1

2. Verify robot is not in error state:
   ```python
   robot.clear_errors()
   ```

3. Check safety limits aren't blocking motion
4. Verify robot is initialized and ready
5. Check collision detection isn't triggered

### Movements are jerky or laggy

**Solutions**:
1. Use wired connection instead of WiFi
2. Reduce update rate:
   ```yaml
   control:
     update_rate: 50  # Reduce from 100
   ```

3. Increase smoothing in velocity control
4. Close unnecessary applications
5. Check system CPU usage

### Robot moves too fast/slow

**Solutions**:
1. Adjust speed in configuration:
   ```yaml
   speeds:
     linear: 0.05  # Reduce speed
     angular: 0.2
   ```

2. Use speed adjustment keys:
   - Keyboard: +/- keys
   - Joystick: Use normal vs turbo mode

3. Adjust velocity limits in robot configuration

### Emergency stop doesn't work

**Solutions**:
1. Verify button mapping is correct
2. Check pygame event processing
3. Use physical emergency stop button on robot
4. Send stop command directly:
   ```python
   robot.stop()
   ```

## Safety Issues

### Collision detection too sensitive

**Solutions**:
1. Reduce collision level:
   ```python
   robot.set_collision_level(1)  # 0-8, lower = less sensitive
   ```

2. Adjust in configuration:
   ```yaml
   safety:
     collision_level: 1
   ```

### Robot hits workspace limits

**Solutions**:
1. Adjust workspace limits in configuration:
   ```yaml
   limits:
     workspace:
       x_min: -0.6
       x_max: 0.6
       # etc.
   ```

2. Move robot to safer starting position
3. Recalibrate workspace for your setup

## Software Issues

### Import errors

**Symptoms**: `ModuleNotFoundError` or import failures

**Solutions**:
1. Verify virtual environment is activated:
   ```bash
   source venv/bin/activate
   ```

2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

3. Install RealMan API:
   ```bash
   pip install Robotic_Arm
   ```

4. Check Python version:
   ```bash
   python --version  # Should be 3.9+
   ```

### Pygame errors

**Solutions**:
1. Install pygame:
   ```bash
   pip install pygame
   ```

2. Install system dependencies (Linux):
   ```bash
   sudo apt-get install python3-pygame
   ```

3. Reinstall pygame:
   ```bash
   pip uninstall pygame
   pip install pygame
   ```

### Permission errors (Linux)

**Solutions**:
1. Add user to input group:
   ```bash
   sudo usermod -a -G input $USER
   # Log out and back in
   ```

2. Run with sudo (not recommended for production):
   ```bash
   sudo python examples/keyboard_teleop.py
   ```

## Performance Issues

### High CPU usage

**Solutions**:
1. Reduce update rate
2. Disable debug logging
3. Close unnecessary applications
4. Use faster computer

### Memory leaks

**Solutions**:
1. Restart script periodically
2. Update to latest version
3. Check for circular references
4. Report issue on GitHub

## Getting Help

If issues persist:

1. **Check logs**: Enable DEBUG logging
   ```bash
   python examples/keyboard_teleop.py --log-level DEBUG
   ```

2. **Test with simple example**:
   ```python
   python examples/basic_usage.py
   ```

3. **Check RealMan documentation**:
   - https://develop.realman-robotics.com/

4. **Report issues**:
   - GitHub Issues: [link]
   - Include error messages, logs, and system info

5. **Contact RealMan support**:
   - Email: sales@realman-robot.com
   - RealMan Academy: https://blog.csdn.net/realman_Rop
