"""
Utility Functions Module

Helper functions for robot teleoperation.
"""

import logging
import math
from typing import List, Tuple

logger = logging.getLogger(__name__)


def setup_logging(level: str = "INFO", log_file: str = None):
    """
    Setup logging configuration.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path
    """
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {level}')
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    root_logger.addHandler(console_handler)
    
    # File handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)


def degrees_to_radians(degrees: List[float]) -> List[float]:
    """Convert degrees to radians."""
    return [math.radians(d) for d in degrees]


def radians_to_degrees(radians: List[float]) -> List[float]:
    """Convert radians to degrees."""
    return [math.degrees(r) for r in radians]


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp value between min and max."""
    return max(min(value, max_val), min_val)


def apply_deadzone(value: float, deadzone: float) -> float:
    """Apply deadzone to input value."""
    if abs(value) < deadzone:
        return 0.0
    # Scale to full range after deadzone
    sign = 1 if value > 0 else -1
    return sign * (abs(value) - deadzone) / (1.0 - deadzone)


def smooth_velocity(
    current: List[float],
    target: List[float],
    smoothing: float = 0.5
) -> List[float]:
    """
    Apply exponential smoothing to velocity.
    
    Args:
        current: Current velocity
        target: Target velocity
        smoothing: Smoothing factor (0-1, higher = smoother)
        
    Returns:
        Smoothed velocity
    """
    return [
        smoothing * current[i] + (1 - smoothing) * target[i]
        for i in range(len(current))
    ]


def normalize_vector(vector: List[float]) -> List[float]:
    """Normalize vector to unit length."""
    magnitude = math.sqrt(sum(v**2 for v in vector))
    if magnitude > 0:
        return [v / magnitude for v in vector]
    return vector


def vector_magnitude(vector: List[float]) -> float:
    """Calculate vector magnitude."""
    return math.sqrt(sum(v**2 for v in vector))


def limit_vector_magnitude(vector: List[float], max_magnitude: float) -> List[float]:
    """Limit vector magnitude to maximum value."""
    magnitude = vector_magnitude(vector)
    if magnitude > max_magnitude:
        scale = max_magnitude / magnitude
        return [v * scale for v in vector]
    return vector


def pose_to_string(pose: List[float]) -> str:
    """Format pose as readable string."""
    if len(pose) >= 6:
        return (f"Position: ({pose[0]:.3f}, {pose[1]:.3f}, {pose[2]:.3f}) m, "
                f"Orientation: ({pose[3]:.3f}, {pose[4]:.3f}, {pose[5]:.3f}) rad")
    return str(pose)


def joints_to_string(joints: List[float]) -> str:
    """Format joint angles as readable string."""
    return "Joints: [" + ", ".join(f"{j:.2f}°" for j in joints) + "]"


class RateLimiter:
    """Simple rate limiter for periodic operations."""
    
    def __init__(self, rate_hz: float):
        """
        Initialize rate limiter.
        
        Args:
            rate_hz: Desired rate in Hz
        """
        import time
        self.period = 1.0 / rate_hz
        self.last_time = time.time()
    
    def sleep(self):
        """Sleep to maintain desired rate."""
        import time
        elapsed = time.time() - self.last_time
        if elapsed < self.period:
            time.sleep(self.period - elapsed)
        self.last_time = time.time()
