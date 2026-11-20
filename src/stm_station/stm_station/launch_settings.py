# Course source: https://github.com/Robolabo/ROS_course
# Upstream revision: cf9e122904ebcb55d336aa7e82d0760bc94cbb07
# Template: Templates/stm_station_launch.py
# Template: Templates/stm_station_launch_all.py
# DONE marks code implementation, not a successful ROS/hardware test.
# Team launch/helper code adapts the listed course pattern; no separate numbered scaffold exists.
"""Validation shared by installed launch descriptions (no ROS imports)."""

# Team helper for the namespace-building step in the course launch templates.
def group_namespace(group_id):
    group_id = int(group_id)
    if group_id <= 0:
        raise ValueError('Group IDs must be positive integers')
    return f'group_{group_id}'


def validate_pair(master, slave, master_port, slave_port, start_slave):
    group_namespace(master)
    group_namespace(slave)
    if int(master) == int(slave):
        raise ValueError('Master and slave group IDs must differ')
    if not master_port.strip():
        raise ValueError('The master serial port is required')
    if start_slave and (not slave_port.strip() or master_port == slave_port):
        raise ValueError('Use a distinct nonempty slave port when start_slave is true')
