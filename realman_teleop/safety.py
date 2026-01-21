"""
Safety Monitor Module

Safety features and monitoring for robot teleoperation.
"""

import logging
from typing import Dict, List, Optional
from .robot_controller import RobotController

logger = logging.getLogger(__name__)


class SafetyMonitor:
    """
    Safety monitoring and enforcement for robot teleoperation.
    
    Provides features like velocity limiting, workspace limits,
    collision detection, and emergency stop handling.
    """
    
    def __init__(
        self,
        robot: RobotController,
        enable_velocity_limits: bool = True,
        enable_workspace_limits: bool = True,
        enable_collision_detection: bool = True,
    ):
        """
        Initialize safety monitor.
        
        Args:
            robot: RobotController instance
            enable_velocity_limits: Enable velocity limiting
            enable_workspace_limits: Enable workspace boundary checks
            enable_collision_detection: Enable collision detection
        """
        self.robot = robot
        self.enable_velocity_limits = enable_velocity_limits
        self.enable_workspace_limits = enable_workspace_limits
        self.enable_collision_detection = enable_collision_detection
        
        # Default safety limits
        self.max_linear_velocity = 0.5  # m/s
        self.max_angular_velocity = 1.0  # rad/s
        self.max_joint_velocity = 30.0  # deg/s
        
        # Workspace limits (example for RM65, adjust per model)
        self.workspace_limits = {
            'x': (-0.7, 0.7),
            'y': (-0.7, 0.7),
            'z': (0.0, 1.0),
        }
        
        # Collision detection level
        self.collision_level = 3
        
        # Safety state
        self.violations = []
        self.emergency_stop_triggered = False
        
        logger.info("Safety monitor initialized")
        self._log_safety_config()
    
    def _log_safety_config(self):
        """Log current safety configuration."""
        logger.info("Safety Configuration:")
        logger.info(f"  Velocity limits: {self.enable_velocity_limits}")
        logger.info(f"  Workspace limits: {self.enable_workspace_limits}")
        logger.info(f"  Collision detection: {self.enable_collision_detection}")
        logger.info(f"  Max linear velocity: {self.max_linear_velocity} m/s")
        logger.info(f"  Max angular velocity: {self.max_angular_velocity} rad/s")
        logger.info(f"  Max joint velocity: {self.max_joint_velocity} deg/s")
    
    def check_commands(self, commands: Dict) -> Dict:
        """
        Check and enforce safety on commands.
        
        Args:
            commands: Command dictionary from control mode
            
        Returns:
            Modified commands with safety enforced, or emergency stop
        """
        self.violations.clear()
        
        if self.emergency_stop_triggered:
            return {'type': 'stop', 'reason': 'emergency_stop'}
        
        # Check velocity limits
        if self.enable_velocity_limits:
            commands = self._check_velocity_limits(commands)
        
        # Check workspace limits
        if self.enable_workspace_limits:
            commands = self._check_workspace_limits(commands)
        
        # Log violations
        if self.violations:
            logger.warning(f"Safety violations: {', '.join(self.violations)}")
        
        return commands
    
    def _check_velocity_limits(self, commands: Dict) -> Dict:
        """Check and enforce velocity limits."""
        if commands.get('type') == 'cartesian':
            target_pose = commands.get('target', [])
            if len(target_pose) >= 6:
                # Check if target would require excessive velocity
                current_pose = self.robot.get_current_pose()
                if current_pose:
                    dt = 0.01  # Assumed time step
                    
                    # Linear velocity check
                    linear_vel = [
                        abs((target_pose[i] - current_pose[i]) / dt)
                        for i in range(3)
                    ]
                    if max(linear_vel) > self.max_linear_velocity:
                        self.violations.append("linear_velocity_exceeded")
                        # Scale down
                        scale = self.max_linear_velocity / max(linear_vel)
                        commands['target'][:3] = [
                            current_pose[i] + (target_pose[i] - current_pose[i]) * scale
                            for i in range(3)
                        ]
                    
                    # Angular velocity check
                    angular_vel = [
                        abs((target_pose[i] - current_pose[i]) / dt)
                        for i in range(3, 6)
                    ]
                    if max(angular_vel) > self.max_angular_velocity:
                        self.violations.append("angular_velocity_exceeded")
                        scale = self.max_angular_velocity / max(angular_vel)
                        commands['target'][3:] = [
                            current_pose[i] + (target_pose[i] - current_pose[i]) * scale
                            for i in range(3, 6)
                        ]
        
        elif commands.get('type') == 'joint':
            target_joints = commands.get('target', [])
            if target_joints:
                current_joints = self.robot.get_current_joint_angles()
                if current_joints:
                    dt = 0.01
                    joint_vel = [
                        abs((target_joints[i] - current_joints[i]) / dt)
                        for i in range(len(target_joints))
                    ]
                    if max(joint_vel) > self.max_joint_velocity:
                        self.violations.append("joint_velocity_exceeded")
                        scale = self.max_joint_velocity / max(joint_vel)
                        commands['target'] = [
                            current_joints[i] + (target_joints[i] - current_joints[i]) * scale
                            for i in range(len(target_joints))
                        ]
        
        return commands
    
    def _check_workspace_limits(self, commands: Dict) -> Dict:
        """Check workspace boundaries."""
        if commands.get('type') == 'cartesian':
            target_pose = commands.get('target', [])
            if len(target_pose) >= 3:
                # Check X, Y, Z limits
                axes = ['x', 'y', 'z']
                for i, axis in enumerate(axes):
                    min_val, max_val = self.workspace_limits[axis]
                    if target_pose[i] < min_val:
                        self.violations.append(f"{axis}_min_exceeded")
                        target_pose[i] = min_val
                    elif target_pose[i] > max_val:
                        self.violations.append(f"{axis}_max_exceeded")
                        target_pose[i] = max_val
                
                commands['target'] = target_pose
        
        return commands
    
    def trigger_emergency_stop(self):
        """Trigger emergency stop."""
        logger.critical("EMERGENCY STOP TRIGGERED BY SAFETY MONITOR")
        self.emergency_stop_triggered = True
        self.robot.stop()
    
    def reset_emergency_stop(self):
        """Reset emergency stop."""
        logger.info("Emergency stop reset")
        self.emergency_stop_triggered = False
        self.violations.clear()
    
    def set_velocity_limits(
        self,
        linear: Optional[float] = None,
        angular: Optional[float] = None,
        joint: Optional[float] = None
    ):
        """Update velocity limits."""
        if linear is not None:
            self.max_linear_velocity = linear
        if angular is not None:
            self.max_angular_velocity = angular
        if joint is not None:
            self.max_joint_velocity = joint
        
        logger.info(f"Velocity limits updated: linear={self.max_linear_velocity}, "
                   f"angular={self.max_angular_velocity}, joint={self.max_joint_velocity}")
    
    def set_workspace_limits(self, limits: Dict[str, tuple]):
        """
        Update workspace limits.
        
        Args:
            limits: Dictionary with 'x', 'y', 'z' keys and (min, max) tuples
        """
        self.workspace_limits.update(limits)
        logger.info(f"Workspace limits updated: {self.workspace_limits}")
    
    def enable_collision_detection(self, level: int = 3):
        """
        Enable collision detection.
        
        Args:
            level: Collision sensitivity level (0-8, higher = more sensitive)
        """
        if 0 <= level <= 8:
            self.collision_level = level
            result = self.robot.set_collision_level(level)
            if result == 0:
                logger.info(f"Collision detection enabled at level {level}")
            else:
                logger.error("Failed to set collision detection level")
        else:
            logger.error("Collision level must be 0-8")
