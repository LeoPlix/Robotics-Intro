"""
Motion estimation and dead-reckoning module.
Integrates linear acceleration for position tracking with baseline offset
calibration and deadband filtering, and computes orientation from encoder ticks.
"""
import math


class MotionEstimate:
    def __init__(self, calibration_samples=50, acceleration_scale=1.0,
                 deadband=0.5, max_dt=0.2, ticks_per_revolution=24.0,
                 gear_ratio=9.7, encoder_direction=1.0):
        positive = (acceleration_scale, max_dt, ticks_per_revolution, gear_ratio)
        if (not isinstance(calibration_samples, int) or calibration_samples < 1
                or not all(math.isfinite(v) and v > 0 for v in positive)
                or not math.isfinite(deadband) or deadband < 0
                or encoder_direction not in (-1.0, 1.0)):
            raise ValueError('Invalid motion estimator configuration')

        self.calibration_samples = calibration_samples
        self.scale = acceleration_scale
        self.deadband = deadband
        self.max_dt = max_dt
        self.encoder_scale = encoder_direction * math.tau / (ticks_per_revolution * gear_ratio)
        self.reset()

    @property
    def calibrated(self):
        return self.sample_count >= self.calibration_samples

    def reset(self):
        self.position = [0.0] * 3
        self.velocity = [0.0] * 3
        self.offset = [0.0] * 3
        self.sample_count = 0
        self.last_time = None
        self.yaw = 0.0

    def update(self, acceleration, encoder, stamp):
        if len(acceleration) != 3 or not all(
                math.isfinite(v) for v in (*acceleration, encoder, stamp)):
            raise ValueError('Motion samples must be finite')

        scaled = [value * self.scale for value in acceleration]
        if not all(math.isfinite(v) for v in scaled):
            raise ValueError('Scaled acceleration overflow')

        self.yaw = math.remainder(encoder * self.encoder_scale, math.tau)
        if self.last_time is not None and stamp == self.last_time:
            return

        if not self.calibrated:
            self.sample_count += 1
            weight = 1.0 / self.sample_count
            self.offset = [
                current + (incoming - current) * weight
                for current, incoming in zip(self.offset, scaled)
            ]
            self.last_time = stamp
            return

        dt = stamp - self.last_time if self.last_time is not None else 0.0
        self.last_time = stamp
        if dt <= 0.0 or dt > self.max_dt:
            self.velocity = [0.0] * 3
            return

        corrected = [value - bias for value, bias in zip(scaled, self.offset)]
        magnitude = math.sqrt(sum(v * v for v in corrected))
        if magnitude <= self.deadband:
            acceleration_step = [0.0] * 3
        else:
            gain = (magnitude - self.deadband) / magnitude
            acceleration_step = [v * gain for v in corrected]

        for axis in range(3):
            self.velocity[axis] += acceleration_step[axis] * dt
            self.position[axis] += self.velocity[axis] * dt
