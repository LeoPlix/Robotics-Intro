"""
Telemetry state estimation and RViz visualization node alias.
"""
from .visualization_node import STMVisualizationNode, main

__all__ = ['STMVisualizationNode', 'main']

if __name__ == '__main__':
    main()
