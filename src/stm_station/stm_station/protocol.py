# Course source: https://github.com/Robolabo/ROS_course
# Upstream revision: cf9e122904ebcb55d336aa7e82d0760bc94cbb07
# Template: Templates/5_stm_serial_communication_python.py
# Template: Templates/6_stm_serial_node_pub.py
# Template: Templates/7_stm_serial_node_pub_sub.py
# Template: Templates/9_stm_control_node_master_slave_poscontrol.py
# Template: Templates/10_stm_control_node_master_slave_impedance_control.py
# DONE marks code implementation, not a successful ROS/hardware test.
"""Course serial protocol and controller math, independent of ROS."""
import math

# Spected format:
# {motor_position, motor_velocity, imu_acceleration_x, imu_acceleration_y, imu_acceleration_z, imu_gyro_x, imu_gyro_y, imu_gyro_z}
# 1. motor_position
# 2. motor_velocity
# 3. imu_acceleration_x
# 4. imu_acceleration_y
# 5. imu_acceleration_z
# 6. imu_gyro_x
# 7. imu_gyro_y
# 8. imu_gyro_z
# ADAPTATION: motor_position is named motor_encoder in STMState.
FIELDS = ('motor_encoder', 'motor_velocity', 'accel_x', 'accel_y',
          'accel_z', 'gyro_x', 'gyro_y', 'gyro_z')


def parse_state(line):
    # Decode the data
    # Remove leading and trailing whitespace
    text = line.decode('utf-8').strip()
    # Check if data is properly formatted with braces
    if not (text.startswith('{') and text.endswith('}')):
        raise ValueError('Expected a brace-delimited state')
    # Split the data by commas, then tranform the string values into floats
    values = [float(value) for value in text[1:-1].split(',')]
    # DONE (template TODO): Ensure the correct number of data parts is present (expected 8 fields) and fill variables
    if len(values) != 8 or not all(math.isfinite(v) and abs(v) <= 3.402823466e38 for v in values):
        raise ValueError('Expected eight finite float32 values')
    return dict(zip(FIELDS, values))


# format: {control_type, goal_position, Kp, PWM}
# control_type: 0 = Stop, 1 = Position Control (Close Loop), 2 = PWM Control (Open Loop)
def encode_control(mode, setpoint, kp, pwm):
    if mode not in (0, 1, 2) or not all(math.isfinite(v) for v in (setpoint, kp, pwm)) or kp < 0:
        raise ValueError('Invalid control command')
    if mode == 0:
        setpoint = kp = pwm = 0.0
    pwm = max(-250.0, min(250.0, pwm))
    # DONE (template TODO): add a newline character to indicate the end of the command
    # Template 6 places this command TODO inside its publisher; it belongs here.
    return f'{{{mode}, {setpoint}, {kp}, {pwm}}}\n'.encode('utf-8')


def feedback_pwm(master, slave, kp, kd, limit):
    # DONE (template TODO): Calculate the error between the master and slave positions
    # DONE (template TODO): Calculate the position error between the master and slave encoder positions
    # DONE (template TODO): Calculate the velocity error between the master and slave encoder velocities
    # DONE (template TODO): Calculate the control command using the proportional gain constant
    # DONE (template TODO): Calculate the control command using the gain constants
    # ADAPTATION: kd=0 gives the template 9 P controller; kd>0 adds template 10 impedance.
    result = kp * (master[0] - slave[0]) + kd * (master[1] - slave[1])
    # Saturate the control command to the valid range
    return max(-limit, min(limit, result))


# Template 7 command fields: control_type, goal_position, Kp, PWM.
def standard_control_values(data):
    """D1.2 array: [mode, setpoint, kp, pwm], rejecting fractional modes."""
    if len(data) != 4 or data[0] not in (0.0, 1.0, 2.0):
        raise ValueError('Expected [mode (0/1/2), setpoint, kp, pwm]')
    values = (int(data[0]), *data[1:])
    encode_control(*values)  # Validate before passing to the serial transport.
    return values
