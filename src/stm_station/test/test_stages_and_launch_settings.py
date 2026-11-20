import pytest

from stm_station.launch_settings import group_namespace, validate_pair
from stm_station.protocol import standard_control_values


@pytest.mark.parametrize('data', [[], [1, 2, 3], [1.5, 0, 1, 0],
                                 [3, 0, 0, 0], [2, 0, 0, float('nan')]])
def test_invalid_standard_control(data):
    with pytest.raises(ValueError):
        standard_control_values(data)


def test_standard_control_preserves_course_array_order():
    assert standard_control_values([1.0, 12.0, 2.0, 0.0]) == (1, 12.0, 2.0, 0.0)


def test_group7_namespace():
    assert group_namespace('7') == 'group_7'


@pytest.mark.parametrize('master,slave,port,slave_port,start', [
    ('7', '7', '/dev/a', '/dev/b', False),
    ('0', '2', '/dev/a', '/dev/b', False),
    ('7', '2', '/dev/a', '/dev/a', True),
    ('7', '2', '', '/dev/b', False),
    ('7', '2', '/dev/a', '', True),
])
def test_invalid_launch_pair(master, slave, port, slave_port, start):
    with pytest.raises(ValueError):
        validate_pair(master, slave, port, slave_port, start)


def test_remote_slave_does_not_need_local_device():
    validate_pair('7', '2', '/dev/a', '', False)
