import math

import pytest

from stm_station.motion import MotionEstimate


def estimate(**kwargs):
    return MotionEstimate(calibration_samples=2, deadband=0.0, max_dt=1.0, **kwargs)


def test_stationary_offset_is_removed_and_encoder_uses_gear_ratio():
    model = estimate()
    model.update((0, 0, 9.81), 0, 1.0)
    model.update((0, 0, 9.81), 0, 1.1)
    model.update((0, 0, 9.81), 24 * 9.7 / 4, 1.2)
    assert model.calibrated
    assert model.position == [0.0, 0.0, 0.0]
    assert model.yaw == pytest.approx(math.pi / 2)


def test_constant_acceleration_integrates_all_axes_and_velocity_coasts():
    model = estimate()
    model.update((0, 0, 0), 0, 1.0)
    model.update((0, 0, 0), 0, 2.0)
    model.update((2, 4, -2), 0, 3.0)
    assert model.position == pytest.approx([1, 2, -1])
    assert model.velocity == pytest.approx([2, 4, -2])
    model.update((0, 0, 0), 0, 4.0)
    assert model.position == pytest.approx([3, 6, -3])


def test_large_gap_and_clock_reversal_do_not_integrate_or_keep_velocity():
    model = estimate()
    for stamp in (1.0, 2.0):
        model.update((0, 0, 0), 0, stamp)
    model.update((2, 0, 0), 0, 3.0)
    position = model.position.copy()
    model.update((100, 0, 0), 0, 10.0)
    assert model.position == position and model.velocity == [0, 0, 0]
    model.update((100, 0, 0), 0, 5.0)
    assert model.position == position and model.velocity == [0, 0, 0]


def test_reset_recalibrates_and_clears_translation():
    model = estimate()
    for stamp in (1.0, 2.0, 3.0):
        model.update((stamp, 0, 0), 1, stamp)
    model.reset()
    assert not model.calibrated
    assert model.position == [0, 0, 0]
    assert model.velocity == [0, 0, 0]
    assert model.last_time is None


def test_invalid_sample_does_not_poison_calibration():
    model = estimate()
    with pytest.raises(ValueError):
        model.update((float('nan'), 0, 0), 0, 1.0)
    assert model.sample_count == 0


@pytest.mark.parametrize('kwargs', [dict(calibration_samples=0), dict(max_dt=0),
                                     dict(ticks_per_revolution=0), dict(gear_ratio=0),
                                     dict(acceleration_scale=float('nan'))])
def test_invalid_configuration(kwargs):
    with pytest.raises(ValueError):
        MotionEstimate(**kwargs)


def test_acceleration_scaling_and_deadband():
    model = MotionEstimate(calibration_samples=1, acceleration_scale=9.81,
                           deadband=0.5, max_dt=1.0)
    model.update((0, 0, 1), 0, 1.0)
    model.update((0.01, 0, 1), 0, 2.0)
    assert model.position == [0, 0, 0]
    model.update((1, 0, 1), 0, 3.0)
    assert model.position[0] == pytest.approx(4.905)
