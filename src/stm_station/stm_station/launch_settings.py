"""
Validation and namespace helper functions for launch files.
"""


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
