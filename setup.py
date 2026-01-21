"""Setup script for RealMan Robot Teleoperation package."""

from setuptools import setup, find_packages
import os

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="realman-teleop",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Teleoperation library for RealMan robotic arms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/realman-teleop",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Robotics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "pylint>=2.12.0",
            "black>=22.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "realman-keyboard=examples.keyboard_teleop:main",
            "realman-joystick=examples.joystick_teleop:main",
            "realman-list-joysticks=examples.list_joysticks:main",
        ],
    },
    include_package_data=True,
    package_data={
        "realman_teleop": ["config/*.yaml"],
    },
)
