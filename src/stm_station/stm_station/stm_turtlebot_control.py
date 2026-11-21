"""
TurtleBot teleoperation control node alias.
"""
from .turtlebot_control import STMTurtleBotControlNode, main

__all__ = ['STMTurtleBotControlNode', 'main']

if __name__ == '__main__':
    main()
