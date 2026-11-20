import pytest
from stm_station.protocol import parse_state, encode_control, feedback_pwm


def test_state_mapping():
    state = parse_state(b'{1,2,3,4,5,6,7,8}\r\n')
    assert state['motor_encoder'] == 1 and state['gyro_z'] == 8


@pytest.mark.parametrize('line', [b'1,2', b'{1,2}', b'{nan,2,3,4,5,6,7,8}', b'{1e100,2,3,4,5,6,7,8}'])
def test_invalid_state(line):
    with pytest.raises(ValueError):
        parse_state(line)


def test_commands():
    assert encode_control(0, 99, 2, 10) == b'{0, 0.0, 0.0, 0.0}\n'
    assert encode_control(2, 0, 0, 999) == b'{2, 0, 0, 250.0}\n'
    with pytest.raises(ValueError):
        encode_control(3, 0, 0, 0)


def test_position_and_impedance():
    assert feedback_pwm((10, 4), (3, 1), 2, 0, 250) == 14
    assert feedback_pwm((10, 4), (3, 1), 2, 3, 250) == 23
    assert feedback_pwm((100, 0), (0, 0), 10, 0, 250) == 250
    assert feedback_pwm((-100, 0), (0, 0), 10, 0, 250) == -250
