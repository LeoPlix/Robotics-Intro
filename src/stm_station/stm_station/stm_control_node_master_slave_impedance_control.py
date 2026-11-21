"""
Master-slave impedance (PD) control node alias.
"""
from .control_node import STMControlNode, main

__all__ = ['STMControlNode', 'main']

if __name__ == '__main__':
    main()
