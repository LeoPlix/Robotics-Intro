"""Check the actual setuptools data_files used for colcon installation."""
import runpy
from pathlib import Path

import setuptools


def test_launch_config_and_stage_entry_points_are_packaged(monkeypatch):
    package = Path(__file__).resolve().parents[1]
    captured = {}
    monkeypatch.chdir(package)
    monkeypatch.setattr(setuptools, 'setup', lambda **kwargs: captured.update(kwargs))
    runpy.run_path(str(package / 'setup.py'))
    assets = {dest: [Path(path).as_posix() for path in paths]
              for dest, paths in captured['data_files']}
    assert set(assets['share/stm_station/launch']) == {
        'launch/stm_serial_node_launch.py', 'launch/stm_serial_control_launch.py',
        'launch/stm_visualization_launch.py', 'launch/stm_bug0_launch.py',
        'launch/stm_station_launch.py', 'launch/stm_station_launch_all.py'}
    assert assets['share/stm_station/rviz'] == ['rviz/stm_config.rviz']
    assert set(assets['share/stm_station/config']) == {'config/serial_params.yaml', 'config/bug0_params.yaml'}
    entrypoints = captured['entry_points']['console_scripts']
    assert len(entrypoints) == 10
    for entry in entrypoints:
        module, function = entry.split(' = ')[1].split(':')
        assert (package / (module.replace('.', '/') + '.py')).exists()
