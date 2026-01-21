#!/usr/bin/env python3
"""
List Joysticks Utility

Lists all available joystick/gamepad devices.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from realman_teleop.joystick_teleop import list_joysticks


def main():
    """Main function."""
    print("=" * 60)
    print("RealMan Robot - Joystick Device Listing")
    print("=" * 60)
    
    list_joysticks()
    
    print("\n" + "=" * 60)
    print("Use the device index with --device flag when running joystick_teleop.py")
    print("Example: python joystick_teleop.py --device 0")
    print("=" * 60)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
