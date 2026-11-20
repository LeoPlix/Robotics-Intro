# Course source: https://github.com/Robolabo/ROS_course
# Upstream revision: cf9e122904ebcb55d336aa7e82d0760bc94cbb07
# Template: Templates/13_bug0_lidar_stm.py
# DONE marks code implementation, not a successful ROS/hardware test.
"""Course-style reactive Bug0 decisions, independent of ROS transport."""
from dataclasses import dataclass
import math
from typing import Optional


@dataclass(frozen=True)
# Template 13, step 2.5: latest minimum distance for right, front and left.
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


# Step 3: Define a helper function to get the minimum valid distance in one LiDAR section
def scan_sectors(ranges, angle_min, angle_increment, range_min, range_max,
                 min_valid_fraction=0.5):
    """Front +/-30 degrees, left 30..90, right -90..-30 in scan frame.

    +inf is a normal no-return up to range_max; NaN/invalid high values
    are unknown. Sub-minimum readings conservatively count as zero clearance.
    """
    if (not all(math.isfinite(v) for v in (angle_min, angle_increment, range_min, range_max))
            or angle_increment == 0 or range_min < 0 or range_max <= range_min
            or not 0 < min_valid_fraction <= 1):
        raise ValueError('Invalid scan geometry or coverage threshold')
    # Step 4.1: Compute how many LiDAR samples belong to each section
    # DONE (template TODO): Step 4.2 Split the LiDAR vector into right, front, and left sections
    # Hint: 10 Hz means a period of 0.1 seconds
    #   - first third  -> right side
    #   - middle third -> front
    #   - last third   -> left side
    # ADAPTATION: The first/middle/last-third hint assumes a forward-facing scan.
    # Use scan angles for +/-30 front and 30..90 side sectors in a 360-degree scan.
    counts = [0, 0, 0]
    values = [[], [], []]
    for index, distance in enumerate(ranges):
        angle = math.remainder(angle_min + index * angle_increment, math.tau)
        if abs(angle) <= math.pi / 6:
            sector = 1
        elif -math.pi / 2 <= angle < -math.pi / 6:
            sector = 0
        elif math.pi / 6 < angle <= math.pi / 2:
            sector = 2
        else:
            continue
        counts[sector] += 1
        if distance == math.inf:
            values[sector].append(range_max)
        elif distance == -math.inf or (math.isfinite(distance) and distance < range_min):
            values[sector].append(0.0)
        elif math.isfinite(distance) and distance <= range_max:
            values[sector].append(distance)
    # DONE (template TODO): Step 4.3 Compute the minimum distance in each section
    minima = [min(data) if count and len(data) / count >= min_valid_fraction else None
              for data, count in zip(values, counts)]
    return Sectors(*minima)


class Bug0Policy:
    def __init__(self, obstacle_distance=1.0, release_distance=1.2,
                 linear_speed=0.3, angular_speed=0.5, turn_clearance=0.4):
        values = (obstacle_distance, release_distance, linear_speed, angular_speed, turn_clearance)
        if (not all(math.isfinite(v) and v > 0 for v in values)
                or release_distance < obstacle_distance or turn_clearance > obstacle_distance):
            raise ValueError('Invalid Bug0 parameters')
        self.obstacle_distance = obstacle_distance
        self.release_distance = release_distance
        self.linear_speed = linear_speed
        self.angular_speed = angular_speed
        self.turn_clearance = turn_clearance
        self.reset()

    def reset(self):
        self.turn = 0

    # DONE (template TODO): Step 5.5 Complete the Bug0 logic
    # If there is no obstacle in front, move forward using the fixed linear speed
    # and the forward PWM value.
    # Otherwise, turn towards the side with more free space using the fixed angular
    # speed and the turning PWM value.
    # ADAPTATION: Hysteresis retains a turn until front clearance exceeds release_distance;
    # missing sectors or insufficient side clearance stop instead of moving blindly.
    def command(self, sectors):
        if sectors is None or not sectors.complete:
            self.reset()
            return Drive()
        if min(sectors.left, sectors.right) < self.turn_clearance:
            self.reset()
            return Drive()
        threshold = self.release_distance if self.turn else self.obstacle_distance
        if sectors.front > threshold:
            self.reset()
            return Drive(self.linear_speed, 0.0, 'forward')
        if not self.turn:
            self.turn = 1 if sectors.left >= sectors.right else -1
        return Drive(0.0, self.turn * self.angular_speed, 'left' if self.turn > 0 else 'right')


class ScanWatchdog:
    """Reject stale/old scans; wall-clock expiry also works with paused /clock."""
    def __init__(self, timeout=0.5):
        if not math.isfinite(timeout) or timeout <= 0:
            raise ValueError('scan_timeout must be positive')
        self.timeout = timeout
        self.sectors = None
        self.received = None
        self.stamp = None
        self.last_ros_time = None
        self.armed = False

    def invalidate(self):
        self.sectors = self.received = None
        self.armed = False

    def arm(self, enable, wall_time, ros_time):
        self.armed = bool(enable and self.current(wall_time, ros_time) is not None)
        return not enable or self.armed

    def clock(self, ros_time):
        if self.last_ros_time is not None and ros_time < self.last_ros_time:
            self.invalidate()
            self.stamp = None
        self.last_ros_time = ros_time

    def accept(self, sectors, stamp, ros_time, wall_time):
        self.clock(ros_time)
        if self.armed:
            self.current(wall_time, ros_time)  # Latch expiry before replacing data.
        valid = (sectors.complete and (stamp == 0 or
                 (-0.1 <= ros_time - stamp <= self.timeout
                  and (self.stamp is None or stamp > self.stamp))))
        if not valid:
            self.invalidate()
            return False
        # DONE (template TODO): Step 4.4 Store the minimum distances in the node variables
        self.sectors, self.received = sectors, wall_time
        self.stamp = stamp if stamp != 0 else None
        return True

    def current(self, wall_time, ros_time):
        self.clock(ros_time)
        if (self.received is None or wall_time - self.received > self.timeout
                or (self.stamp is not None and ros_time - self.stamp > self.timeout)):
            self.invalidate()
            return None
        return self.sectors
