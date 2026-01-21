"""
Control Modes Module

Different control modes for robot teleoperation.
"""

import logging
from abc import ABC, abstractmethod
from typing import List, Optional

logger = logging.getLogger(__name__)


class ControlMode(ABC):
    """Base class for control modes."""
    
    @abstractmethod
    def compute_command(self, input_velocity: List[float], current_state: dict) -> dict:
        """Compute robot command from input velocity."""
        pass


class JointControl(ControlMode):
    """
    Joint space control mode.
    
    Directly controls individual joint angles.
    """
    
    def __init__(self, max_joint_velocity: float = 30.0):
        """
        Initialize joint control.
        
        Args:
            max_joint_velocity: Maximum joint velocity in deg/s
        """
        self.max_joint_velocity = max_joint_velocity
    
    def compute_command(self, input_velocity: List[float], current_state: dict) -> dict:
        """
        Compute joint command.
        
        Args:
            input_velocity: Desired joint velocities
            current_state: Current robot state
            
        Returns:
            Command dictionary with target joint angles
        """
        current_joints = current_state.get('joint_angles', [])
        if not current_joints:
            logger.warning("No current joint angles available")
            return {'type': 'joint', 'target': []}
        
        # Limit velocities
        limited_velocities = [
            max(min(v, self.max_joint_velocity), -self.max_joint_velocity)
            for v in input_velocity
        ]
        
        # Compute target angles (simple integration)
        dt = current_state.get('dt', 0.01)
        target_joints = [
            current_joints[i] + limited_velocities[i] * dt
            for i in range(len(current_joints))
        ]
        
        return {
            'type': 'joint',
            'target': target_joints,
            'velocity': 50,  # Planning velocity percentage
        }


class CartesianControl(ControlMode):
    """
    Cartesian space control mode.
    
    Controls end-effector position and orientation in 3D space.
    """
    
    def __init__(
        self,
        max_linear_velocity: float = 0.5,
        max_angular_velocity: float = 1.0
    ):
        """
        Initialize Cartesian control.
        
        Args:
            max_linear_velocity: Maximum linear velocity in m/s
            max_angular_velocity: Maximum angular velocity in rad/s
        """
        self.max_linear_velocity = max_linear_velocity
        self.max_angular_velocity = max_angular_velocity
    
    def compute_command(self, input_velocity: List[float], current_state: dict) -> dict:
        """
        Compute Cartesian command.
        
        Args:
            input_velocity: Desired Cartesian velocities [vx, vy, vz, wx, wy, wz]
            current_state: Current robot state
            
        Returns:
            Command dictionary with target pose
        """
        current_pose = current_state.get('pose', [])
        if not current_pose or len(current_pose) != 6:
            logger.warning("No valid current pose available")
            return {'type': 'cartesian', 'target': []}
        
        # Limit velocities
        limited_velocity = [
            max(min(input_velocity[i], self.max_linear_velocity), -self.max_linear_velocity)
            if i < 3 else
            max(min(input_velocity[i], self.max_angular_velocity), -self.max_angular_velocity)
            for i in range(6)
        ]
        
        # Compute target pose
        dt = current_state.get('dt', 0.01)
        target_pose = [
            current_pose[i] + limited_velocity[i] * dt
            for i in range(6)
        ]
        
        return {
            'type': 'cartesian',
            'target': target_pose,
            'velocity': 50,
        }


class VelocityControl(ControlMode):
    """
    Velocity control mode.
    
    Continuous velocity-based control (for advanced users).
    """
    
    def __init__(
        self,
        max_velocity: float = 0.5,
        smoothing_factor: float = 0.5
    ):
        """
        Initialize velocity control.
        
        Args:
            max_velocity: Maximum velocity magnitude
            smoothing_factor: Velocity smoothing (0-1, higher = smoother)
        """
        self.max_velocity = max_velocity
        self.smoothing_factor = smoothing_factor
        self.previous_velocity = [0.0] * 6
    
    def compute_command(self, input_velocity: List[float], current_state: dict) -> dict:
        """
        Compute velocity command with smoothing.
        
        Args:
            input_velocity: Desired velocity
            current_state: Current robot state
            
        Returns:
            Command dictionary with smoothed velocity
        """
        # Apply exponential smoothing
        smoothed_velocity = [
            self.smoothing_factor * self.previous_velocity[i] +
            (1 - self.smoothing_factor) * input_velocity[i]
            for i in range(len(input_velocity))
        ]
        
        # Limit magnitude
        magnitude = sum(v**2 for v in smoothed_velocity) ** 0.5
        if magnitude > self.max_velocity:
            scale = self.max_velocity / magnitude
            smoothed_velocity = [v * scale for v in smoothed_velocity]
        
        self.previous_velocity = smoothed_velocity
        
        return {
            'type': 'velocity',
            'velocity': smoothed_velocity,
        }
