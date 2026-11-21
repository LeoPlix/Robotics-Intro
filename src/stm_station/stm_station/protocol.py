"""
Serial framing protocol and controller math helpers.
"""
import math

FIELDS = (
    'motor_encoder', 'motor_velocity', 'accel_x', 'accel_y',
    'accel_z', 'gyro_x', 'gyro_y', 'gyro_z'
)


def parse_state(line):
    """
    Parses a raw serial line formatted as '{v0, v1, ..., v7}\\n'
    into a dictionary mapped by telemetry field names.
    """
    text = line.decode('utf-8').strip()
    if not (text.startswith('{') and text.endswith('}')):
        raise ValueError('Expected a brace-delimited state')

    values = [float(value) for value in text[1:-1].split(',')]
    if len(values) != 8 or not all(math.isfinite(v) and abs(v) <= 3.402823466e38 for v in values):
        raise ValueError('Expected eight finite float32 values')
    return dict(zip(FIELDS, values))


def encode_control(mode, setpoint, kp, pwm):
    """
    Encodes control command variables into a framed UTF-8 byte string:
    '{control_type, goal_position, kp, pwm}\\n'
    """
    if mode not in (0, 1, 2) or not all(math.isfinite(v) for v in (setpoint, kp, pwm)) or kp < 0:
        raise ValueError('Invalid control command')
    if mode == 0:
        setpoint = kp = pwm = 0.0
    pwm = max(-250.0, min(250.0, pwm))
    return f'{{{mode}, {setpoint}, {kp}, {pwm}}}\n'.encode('utf-8')


def feedback_pwm(master, slave, kp, kd, limit):
    """
    Computes proportional-derivative control output with saturation clamp.
    """
    result = kp * (master[0] - slave[0]) + kd * (master[1] - slave[1])
    return max(-limit, min(limit, result))


def standard_control_values(data):
    """
    Validates standard control array: [mode (0/1/2), setpoint, kp, pwm].
    """
    if len(data) != 4 or data[0] not in (0.0, 1.0, 2.0):
        raise ValueError('Expected [mode (0/1/2), setpoint, kp, pwm]')
    values = (int(data[0]), *data[1:])
    encode_control(*values)
    return values
