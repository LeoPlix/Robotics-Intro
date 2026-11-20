"""Construct course launch actions without opening a serial port.

Skipped without ROS; hardware operation is not tested here.
"""
import importlib.util
from pathlib import Path

import pytest

pytest.importorskip('launch')
pytest.importorskip('launch_ros')
from launch_ros.actions import Node


@pytest.mark.parametrize('name,count', [
    ('stm_station_launch.py', 2),
    ('stm_station_launch_all.py', 4),
    ('stm_serial_control_launch.py', 2),
    ('stm_visualization_launch.py', 4),
    ('stm_serial_node_launch.py', 1),
    ('stm_bug0_launch.py', 1),
])
def test_launch_constructs_real_ros_actions(monkeypatch, name, count):
    package = Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location(name, package / 'launch' / name)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if hasattr(module, 'get_package_share_directory'):
        monkeypatch.setattr(module, 'get_package_share_directory', lambda _: str(package))
    description = module.generate_launch_description()
    assert len(description.entities) == count
    assert all(isinstance(action, Node) for action in description.entities)
