"""
Configuration Loader Module

Load and parse YAML configuration files and environment variables.
"""

import logging
import yaml
import os
from pathlib import Path
from typing import Dict, Optional
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class ConfigLoader:
    """Configuration file loader for robot teleoperation."""
    
    @staticmethod
    def load_env_config() -> Dict:
        """
        Load configuration from robot.yaml or .env file.
        Priority: robot.yaml > .env > defaults
        
        Returns:
            Configuration dictionary
        """
        project_root = Path(__file__).parent.parent
        
        # Try robot.yaml first (preferred)
        robot_yaml = project_root / "robot.yaml"
        if robot_yaml.exists():
            try:
                config = ConfigLoader.load_yaml(str(robot_yaml))
                if config:
                    logger.info(f"Loaded configuration from {robot_yaml}")
                    # Ensure all required keys exist with defaults
                    defaults = ConfigLoader.get_default_robot_config()
                    for key in defaults:
                        if key not in config:
                            config[key] = defaults[key]
                    return config
            except Exception as e:
                logger.warning(f"Failed to load robot.yaml: {e}, falling back to .env")
        
        # Fall back to .env file for backwards compatibility
        env_file = project_root / ".env"
        if env_file.exists():
            load_dotenv(env_file)
            logger.info(f"Loaded environment from {env_file}")
        
        # Build config from environment variables or defaults
        config = {
            'robot': {
                'ip': os.getenv('ROBOT_IP', '192.168.10.18'),
                'port': int(os.getenv('ROBOT_PORT', '8080')),
                'model': os.getenv('ROBOT_MODEL', 'R1D2'),
            },
            'control': {
                'update_rate': float(os.getenv('DEFAULT_UPDATE_RATE', '100')),
            },
            'speeds': {
                'default': float(os.getenv('DEFAULT_SPEED', '0.1')),
            },
            'logging': {
                'level': os.getenv('LOG_LEVEL', 'INFO'),
            }
        }
        
        # Add DOF if specified (optional, will auto-detect if not set)
        dof_env = os.getenv('ROBOT_DOF', '')
        if dof_env and dof_env.isdigit():
            config['robot']['dof'] = int(dof_env)
        
        return config
    
    @staticmethod
    def load_yaml(filepath: str) -> Optional[Dict]:
        """
        Load YAML configuration file.
        
        Args:
            filepath: Path to YAML file
            
        Returns:
            Configuration dictionary or None if error
        """
        try:
            with open(filepath, 'r') as f:
                config = yaml.safe_load(f)
            logger.info(f"Loaded configuration from {filepath}")
            return config
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {filepath}")
            return None
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML file: {e}")
            return None
    
    @staticmethod
    def load_robot_config(filepath: str = "config/robot_config.yaml") -> Dict:
        """
        Load robot configuration with priority:
        1. Environment variables (.env file)
        2. YAML config file
        3. Defaults
        """
        # Start with defaults
        config = ConfigLoader.get_default_robot_config()
        
        # Try to load from YAML
        yaml_config = ConfigLoader.load_yaml(filepath)
        if yaml_config:
            # Merge YAML config into defaults
            config.update(yaml_config)
        
        # Load and merge environment variables (highest priority)
        env_config = ConfigLoader.load_env_config()
        if env_config.get('robot'):
            config['robot'].update(env_config['robot'])
        if env_config.get('control'):
            config['control'].update(env_config['control'])
        
        return config
    
    @staticmethod
    def load_keyboard_config(filepath: str = "config/keyboard_config.yaml") -> Dict:
        """Load keyboard configuration with defaults."""
        config = ConfigLoader.load_yaml(filepath)
        if config is None:
            logger.warning("Using default keyboard configuration")
            config = ConfigLoader.get_default_keyboard_config()
        return config
    
    @staticmethod
    def load_joystick_config(filepath: str = "config/joystick_config.yaml") -> Dict:
        """Load joystick configuration with defaults."""
        config = ConfigLoader.load_yaml(filepath)
        if config is None:
            logger.warning("Using default joystick configuration")
            config = ConfigLoader.get_default_joystick_config()
        return config
    
    @staticmethod
    def get_default_robot_config() -> Dict:
        """Get default robot configuration."""
        return {
            'robot': {
                'ip': '192.168.1.18',
                'port': 8080,
                'model': 'RM65',
            },
            'control': {
                'mode': 'cartesian',
                'update_rate': 100,
            },
            'limits': {
                'max_linear_velocity': 0.5,
                'max_angular_velocity': 1.0,
                'max_joint_velocity': 30.0,
            },
            'safety': {
                'enable_deadman': True,
                'enable_collision_detection': True,
                'collision_level': 3,
                'emergency_stop_enabled': True,
            }
        }
    
    @staticmethod
    def get_default_keyboard_config() -> Dict:
        """Get default keyboard configuration."""
        return {
            'keyboard': {
                'forward': 'w',
                'backward': 's',
                'left': 'a',
                'right': 'd',
                'up': 'q',
                'down': 'e',
                'emergency_stop': 'space',
                'enable': 'shift',
            },
            'speeds': {
                'linear': 0.1,
                'angular': 0.3,
                'joint': 10.0,
            }
        }
    
    @staticmethod
    def get_default_joystick_config() -> Dict:
        """Get default joystick configuration."""
        return {
            'joystick': {
                'device': 0,
                'deadzone': 0.1,
            },
            'axes': {
                'linear_x': 1,
                'linear_y': 0,
                'linear_z': 4,
                'angular_x': 3,
                'angular_y': 5,
                'angular_z': 2,
            },
            'buttons': {
                'enable': 4,
                'turbo': 5,
                'emergency_stop': 6,
                'mode_switch': 7,
            },
            'speeds': {
                'normal': {
                    'linear': 0.1,
                    'angular': 0.3,
                },
                'turbo': {
                    'linear': 0.3,
                    'angular': 0.8,
                }
            }
        }
