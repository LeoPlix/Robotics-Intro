"""
Master-slave proportional position control node alias.
"""
from .control_position import STMControlNode, main

__all__ = ['STMControlNode', 'main']

if __name__ == '__main__':
    main()
