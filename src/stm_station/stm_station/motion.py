# Course source: https://github.com/Robolabo/ROS_course
# Upstream revision: cf9e122904ebcb55d336aa7e82d0760bc94cbb07
# Template: Templates/11_stm_visualization.py
# DONE marks code implementation, not a successful ROS/hardware test.
"""Educational fixed-axis IMU integration; not an absolute pose estimator."""
import math

# Template 11, steps 2.3 and 3: numerical state extracted from the ROS callback.
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
        # DONE (template TODO): Step 3.2 Update the rotation based on the received motors turns
        # Change the units from encoder ticks to radians, remember that 1 revolution = 2*pi radians,
        # the reduction ratio is 1:9.7, and the encoder has 24 ticks per revolution
        self.encoder_scale = encoder_direction * math.tau / (ticks_per_revolution * gear_ratio)
        self.reset()

    @property
    def calibrated(self):
        return self.sample_count >= self.calibration_samples

    # Step 2.3: Initialize state variables
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
            return  # A duplicate is not another calibration/integration sample.
        # Step 3.3 Integrate acceleration to get velocity and position
        # Get the elapsed time since the last reading
        # ADAPTATION: Use the source stamp; skip duplicate/reversed stamps and long gaps.
        dt = None if self.last_time is None else stamp - self.last_time
        self.last_time = stamp
        if dt is not None and dt <= 0:
            self.velocity = [0.0] * 3
            return
        # DONE (template TODO): Step 3.2 If it is the first reading, set the offset acceleration
        # ADAPTATION: Average 50 stationary samples rather than a single first sample.
        if not self.calibrated:
            self.sample_count += 1
            for axis in range(3):
                self.offset[axis] += (scaled[axis] - self.offset[axis]) / self.sample_count
            return
        if dt is None or dt > self.max_dt:
            self.velocity = [0.0] * 3
            return
        # DONE (template TODO): Step 3.4 Remove the offset acceleration from the received acceleration
        corrected = [scaled[i] - self.offset[i] for i in range(3)]
        # Step 3.5 Integrate the corrected acceleration to get velocity and position
        # Avoid Drift: Integrate only when the acceleration is greater than a given threshold
        # ADAPTATION: Apply the threshold to acceleration; existing velocity still coasts.
        if math.hypot(*corrected) <= self.deadband:
            corrected = [0.0] * 3
        for axis, value in enumerate(corrected):
            # DONE (template TODO): Integrate the velocity to get the position
            # ADAPTATION: Constant-acceleration position integration precedes the velocity update.
            self.position[axis] += self.velocity[axis] * dt + 0.5 * value * dt * dt
            # Integrate the acceleration to get the position
            self.velocity[axis] += value * dt
