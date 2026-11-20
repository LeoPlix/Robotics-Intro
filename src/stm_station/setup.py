from setuptools import find_packages, setup
from glob import glob
setup(name='stm_station', version='0.1.0', packages=find_packages(),
      data_files=[('share/ament_index/resource_index/packages', ['resource/stm_station']),
                  ('share/stm_station', ['package.xml']),
                  ('share/stm_station/launch', glob('launch/*.py')),
                  ('share/stm_station/rviz', glob('rviz/*.rviz')),
                  ('share/stm_station/config', glob('config/*.yaml'))],
      install_requires=['setuptools', 'pyserial'],
      maintainer='WinningLeos', maintainer_email='athens@todo.todo',
      description='STM serial bridge and controller', license='Proprietary',
      entry_points={'console_scripts': [
          'stm_serial_node_pub = stm_station.serial_publisher_node:main',
          'stm_serial_node_pub_sub = stm_station.serial_pubsub_node:main',
          'stm_serial_node = stm_station.serial_node:main',
          'stm_visualization_node = stm_station.visualization_node:main',
          'bug0_lidar_stm_node = stm_station.bug0_node:main',
          'stm_control_node_master_slave = stm_station.control_master_slave:main',
          'stm_control_node_master_slave_poscontrol = stm_station.control_position:main',
          'stm_control_node_master_slave_impedance_control = stm_station.control_node:main',
          'stm_turtlebot_control_node = stm_station.turtlebot_control:main',
          'stm_control_node = stm_station.control_node:main']})
