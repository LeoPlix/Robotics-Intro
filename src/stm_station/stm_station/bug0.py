"""
Pure-Python reactive Bug0 navigation policy and LaserScan sector processing.
"""
from dataclasses import dataclass
import math
from typing import Optional


@dataclass(frozen=True)
class Sectors:
    right: Optional[float]
    front: Optional[float]
    left: Optional[float]

    @property
    def complete(self):
        return all(v is not None and math.isfinite(v) and v >= 0
                   for v in (self.right, self.front, self.left))


@dataclass(frozen=True)
class Drive:
    linear: float = 0.0
    angular: float = 0.0
    state: str = 'stop'


def scan_sectors(ranges, angle_min, angle_increment, range_min, range_max,
                 min_valid_fraction=0.5):
    """
    Extracts front (+/-30 deg), left (30..90 deg), and right (-90..-30 deg)
    clearance minimums from a LiDAR range scan.
    """
    if (not all(math.isfinite(v) for v in (angle_min, angle_increment, range_min, range_max))
            or angle_increment == 0 or range_min < 0 or range_max <= range_min
            or not 0 < min_valid_fraction <= 1):
        raise ValueError('Invalid scan geometry or coverage threshold')

    count = len(ranges)
    total_coverage = abs(angle_increment) * count
    if total_coverage < math.radians(180):
        raise ValueError('LiDAR scan must cover at least the forward semicircle')

    def sector_range(low_deg, high_deg):
        low, high = sorted((math.radians(low_deg), math.radians(high_deg)))
        readings = []
        for i, val in enumerate(ranges):
            theta = math.remainder(angle_min + i * angle_increment, math.tau)
            if low <= theta <= high:
                readings.append(val)
        if not readings:
            return None
        valid = [r for r in readings if not math.isnan(r) and r >= range_min]
        if len(valid) / len(readings) < min_valid_fraction:
            return None
        finite = [min(r, range_max) for r in valid if math.isfinite(r) and r <= range_max]
        has_submin = any(not math.isnan(r) and r < range_min for r in readings)
        if has_submin:
            return 0.0
        return min(finite) if finite else range_max

    return Sectors(
        right=sector_range(-90, -30),
        front=sector_range(-30, 30),
        left=sector_range(30, 90)
    )


class Bug0Policy:
    def __init__(self, obstacle_distance=1.0, release_distance=1.2,
                 linear_speed=0.3, angular_speed=0.5, turn_clearance=0.4):
        self.obstacle_distance = obstacle_distance
        self.release_distance = release_distance
        self.linear_speed = linear_speed
        self.angular_speed = angular_speed
        self.turn_clearance = turn_clearance
        self.turning = 0

    def command(self, sectors: Sectors) -> Drive:
        if not sectors.complete:
            self.turning = 0
            return Drive(0.0, 0.0, 'stop')

        if min(sectors.left, sectors.right) < self.turn_clearance:
            self.turning = 0
            return Drive(0.0, 0.0, 'stop')

        if self.turning:
            if sectors.front >= self.release_distance:
                self.turning = 0
                return Drive(self.linear_speed, 0.0, 'forward')
            return Drive(0.0, self.turning * self.angular_speed,
                         'turn_left' if self.turning > 0 else 'turn_right')

        if sectors.front > self.obstacle_distance:
            return Drive(self.linear_speed, 0.0, 'forward')

        self.turning = 1 if sectors.left >= sectors.right else -1
        return Drive(0.0, self.turning * self.angular_speed,
                     'turn_left' if self.turning > 0 else 'turn_right')


class ScanWatchdog:
    def __init__(self, timeout=0.5):
        self.timeout = timeout
        self.last_stamp = None

    def valid(self, stamp):
        if not math.isfinite(stamp) or stamp <= 0:
            return False
        if self.last_stamp is not None and (stamp < self.last_stamp or stamp - self.last_stamp > self.timeout):
            return False
        self.last_stamp = stamp
        return True
