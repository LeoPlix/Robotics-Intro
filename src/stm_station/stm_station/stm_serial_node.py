"""
Serial communication bridge node alias using STMState/STMControl.
"""
from .serial_node import SerialPubSubNode, main

__all__ = ['SerialPubSubNode', 'main']

if __name__ == '__main__':
    main()
