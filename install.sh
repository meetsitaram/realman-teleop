#!/bin/bash
# Installation script for RealMan Robot Teleoperation
# This script sets up a conda environment and installs all dependencies

set -e  # Exit on error

echo "=========================================="
echo "RealMan Robot Teleoperation Setup"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo -e "${RED}Error: conda is not installed or not in PATH${NC}"
    echo "Please install Miniconda or Anaconda first:"
    echo "  https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

echo -e "${GREEN}✓ Found conda${NC}"
echo ""

# Check if environment already exists
ENV_NAME="realman-teleop"
if conda env list | grep -q "^${ENV_NAME} "; then
    echo -e "${YELLOW}Environment '${ENV_NAME}' already exists.${NC}"
    read -p "Do you want to remove and recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Removing existing environment..."
        conda env remove -n ${ENV_NAME} -y
    else
        echo "Skipping environment creation. Activating existing environment..."
        echo ""
        echo -e "${GREEN}To activate the environment, run:${NC}"
        echo "  conda activate ${ENV_NAME}"
        exit 0
    fi
fi

# Create conda environment
echo "Creating conda environment from environment.yml..."
conda env create -f environment.yml

echo ""
echo -e "${GREEN}✓ Conda environment created successfully${NC}"
echo ""

# Activate environment and setup configs
echo "Setting up configuration files..."
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate ${ENV_NAME}

# Copy robot.yaml.example if robot.yaml doesn't exist
if [ ! -f "robot.yaml" ]; then
    if [ -f "robot.yaml.example" ]; then
        cp robot.yaml.example robot.yaml
        echo -e "${GREEN}✓ Created robot.yaml configuration file${NC}"
        echo -e "${YELLOW}  → You need to edit robot.yaml with your robot's IP address${NC}"
    fi
else
    echo -e "${YELLOW}⚠ robot.yaml already exists, skipping${NC}"
fi

# Copy example configuration files if they don't exist
if [ ! -f "config/robot_config.yaml" ]; then
    cp config/robot_config.example.yaml config/robot_config.yaml
    echo -e "${GREEN}✓ Created config/robot_config.yaml${NC}"
else
    echo -e "${YELLOW}⚠ config/robot_config.yaml already exists, skipping${NC}"
fi

if [ ! -f "config/keyboard_config.yaml" ]; then
    cp config/keyboard_config.example.yaml config/keyboard_config.yaml
    echo -e "${GREEN}✓ Created config/keyboard_config.yaml${NC}"
else
    echo -e "${YELLOW}⚠ config/keyboard_config.yaml already exists, skipping${NC}"
fi

if [ ! -f "config/joystick_config.yaml" ]; then
    cp config/joystick_config.example.yaml config/joystick_config.yaml
    echo -e "${GREEN}✓ Created config/joystick_config.yaml${NC}"
else
    echo -e "${YELLOW}⚠ config/joystick_config.yaml already exists, skipping${NC}"
fi

echo ""
echo "=========================================="
echo -e "${GREEN}Installation Complete!${NC}"
echo "=========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Activate the environment:"
echo -e "   ${YELLOW}conda activate ${ENV_NAME}${NC}"
echo ""
echo "2. Configure your robot (REQUIRED - only do once):"
echo -e "   ${YELLOW}python setup_robot.py${NC}"
echo "   This will ask for your robot's IP and save it."
echo ""
echo "3. Monitor robot state (RECOMMENDED - safe first step!):"
echo -e "   ${YELLOW}./teleop monitor${NC}"
echo "   Reads robot state without sending commands - verify connection safely"
echo ""
echo "4. Start teleoperation (once confident):"
echo -e "   ${YELLOW}./teleop keyboard${NC}  (for keyboard control)"
echo -e "   ${YELLOW}./teleop joystick${NC}  (for joystick control)"
echo ""
echo "💡 Quick Commands:"
echo "   ./teleop monitor   - Monitor robot (READ-ONLY, safe!)"
echo "   ./teleop keyboard  - Keyboard teleoperation"
echo "   ./teleop joystick  - Joystick teleoperation"
echo "   ./teleop test      - Test robot connection"
echo "   ./teleop list      - List joystick devices"
echo ""
echo "   No need to pass --ip or --model anymore!"
echo ""
echo "🛡️  Tip: Always run './teleop monitor' first to safely verify connection!"
echo ""
echo "⚠️  SAFETY REMINDERS:"
echo "  • Clear the robot workspace before testing"
echo "  • Start with low speeds"
echo "  • Keep emergency stop ready (SPACE key or gamepad Back button)"
echo "  • Always hold deadman switch (SHIFT or LB) to enable motion"
echo ""
echo "For more information, see:"
echo "  • START_HERE.md - Quick start guide"
echo "  • docs/QUICKSTART.md - Detailed setup"
echo "  • docs/TROUBLESHOOTING.md - Common issues"
echo ""
echo "Happy robot teleoperating! 🤖"

