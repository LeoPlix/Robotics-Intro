import math

import pytest

from stm_station.bug0 import Bug0Policy, ScanWatchdog, Sectors, scan_sectors


def scan(values):
    return scan_sectors(values, -math.pi, math.pi / 180, 0.3, 12.0)


def test_full_circle_uses_angles_and_ignores_obstacle_behind():
    values = [5.0] * 360
    values[0] = 0.3  # rear, not front
    values[180] = 0.7
    sectors = scan(values)
    assert sectors.front == 0.7
    assert sectors.left == 5.0 and sectors.right == 5.0


def test_scan_orientation_and_resolution_do_not_change_sector_result():
    values = [5.0] * 361
    values[180] = 0.6
    a = scan_sectors(values, -math.pi, math.pi / 180, 0.3, 12)
    b = scan_sectors(list(reversed(values)), math.pi, -math.pi / 180, 0.3, 12)
    assert a == b


def test_positive_infinity_is_a_valid_no_return_but_nan_is_unknown():
    assert scan([math.inf] * 360).front == 12
    sectors = scan([math.nan] * 360)
    assert sectors.front is None and sectors.left is None
    assert Bug0Policy().command(sectors).state == 'stop'


def test_too_close_reading_is_not_discarded_as_free_space():
    values = [5.0] * 360
    values[180] = 0.01
    assert scan(values).front == 0


def test_missing_sector_or_poor_coverage_stops():
    sectors = scan_sectors([5.0] * 3, -0.01, 0.01, 0.3, 12)
    assert Bug0Policy().command(sectors).state == 'stop'


@pytest.mark.parametrize('angle,increment,low,high', [
    (math.nan, 0.1, 0.3, 12), (0, 0, 0.3, 12),
    (0, 0.1, -1, 12), (0, 0.1, 1, 0.5)])
def test_invalid_scan_geometry(angle, increment, low, high):
    with pytest.raises(ValueError):
        scan_sectors([1, 2, 3], angle, increment, low, high)


def test_forward_turn_direction_hysteresis_and_resume():
    policy = Bug0Policy()
    forward = policy.command(Sectors(right=3, front=3, left=3))
    assert (forward.linear, forward.angular, forward.state) == (0.3, 0.0, 'forward')
    left = policy.command(Sectors(right=1, front=0.7, left=3))
    assert left.linear == 0 and left.angular == 0.5
    # Stay turning until front clears the release distance, even at 1.1 m.
    assert policy.command(Sectors(1, 1.1, 3)).state == 'left'
    assert policy.command(Sectors(1, 1.3, 3)).state == 'forward'
    policy.reset()
    assert policy.command(Sectors(3, 0.7, 1)).angular == -0.5


def test_tie_turns_left_and_blocked_sides_stop():
    policy = Bug0Policy()
    assert policy.command(Sectors(3, 0.5, 3)).state == 'left'
    assert policy.command(Sectors(0.1, 0.5, 0.1)).state == 'stop'
    assert policy.command(None).state == 'stop'


def test_loss_of_side_clearance_cannot_release_forward():
    policy = Bug0Policy()
    assert policy.command(Sectors(0.1, 3, 3)).linear == 0


@pytest.mark.parametrize('kwargs', [dict(linear_speed=-1), dict(angular_speed=0),
                                    dict(obstacle_distance=0), dict(release_distance=0.5),
                                    dict(turn_clearance=2), dict(linear_speed=math.nan)])
def test_invalid_policy_parameters(kwargs):
    with pytest.raises(ValueError):
        Bug0Policy(**kwargs)


def test_watchdog_no_scan_and_wall_timeout_with_paused_simulation():
    watchdog = ScanWatchdog()
    assert watchdog.current(1, 10) is None
    assert watchdog.accept(Sectors(3, 3, 3), 10, 10, 1)
    assert watchdog.current(1.1, 10) is not None
    assert watchdog.current(1.6, 10) is None


def test_watchdog_rejects_old_future_duplicate_and_incomplete_scans():
    watchdog = ScanWatchdog()
    assert not watchdog.accept(Sectors(3, 3, 3), 9, 10, 1)
    assert not watchdog.accept(Sectors(3, 3, 3), 11, 10, 1)
    assert not watchdog.accept(Sectors(3, None, 3), 10, 10, 1)
    assert watchdog.accept(Sectors(3, 3, 3), 10, 10, 1)
    assert not watchdog.accept(Sectors(3, 3, 3), 10, 10.1, 1.1)
    assert watchdog.current(1.1, 10.1) is None


def test_watchdog_ros_expiry_and_clock_reset():
    watchdog = ScanWatchdog()
    assert watchdog.accept(Sectors(3, 3, 3), 10, 10, 1)
    assert watchdog.current(1.1, 11) is None
    assert watchdog.accept(Sectors(3, 3, 3), 1, 1, 2)
    assert watchdog.current(2.1, 1.1) is not None


def test_unstamped_manual_test_scan_uses_arrival_timeout():
    watchdog = ScanWatchdog()
    assert watchdog.accept(Sectors(3, 3, 3), 0, 10, 1)
    assert watchdog.current(1.1, 10.1) is not None
    assert watchdog.current(1.6, 10.1) is None


def test_invalid_then_valid_scan_before_timer_requires_explicit_rearm():
    watchdog = ScanWatchdog()
    assert watchdog.accept(Sectors(3, 3, 3), 10, 10, 1)
    assert watchdog.arm(True, 1, 10)
    assert not watchdog.accept(Sectors(3, None, 3), 10.1, 10.1, 1.1)
    assert watchdog.accept(Sectors(3, 3, 3), 10.2, 10.2, 1.2)
    assert not watchdog.armed
    assert watchdog.arm(True, 1.2, 10.2)


def test_expired_scan_cannot_be_hidden_by_next_receive_before_timer():
    watchdog = ScanWatchdog()
    assert watchdog.accept(Sectors(3, 3, 3), 10, 10, 1)
    assert watchdog.arm(True, 1, 10)
    assert watchdog.accept(Sectors(3, 3, 3), 11, 11, 2)
    assert not watchdog.armed


def test_enable_rejects_no_scan_and_disable_is_always_accepted():
    watchdog = ScanWatchdog()
    assert not watchdog.arm(True, 1, 10)
    assert watchdog.arm(False, 1, 10)
