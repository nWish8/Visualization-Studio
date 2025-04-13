import numpy as np

def create_grid(resolution=64, size=4.0):
    """Create a grid of (resolution x resolution) points in XZ plane"""
    positions = []
    indices = []

    for z in range(resolution):
        for x in range(resolution):
            xpos = (x / (resolution - 1) - 0.5) * size
            zpos = (z / (resolution - 1) - 0.5) * size
            positions.append([xpos, 0.0, zpos])

    for z in range(resolution - 1):
        for x in range(resolution - 1):
            i = z * resolution + x
            indices += [
                i, i + 1, i + resolution,
                i + 1, i + resolution + 1, i + resolution,
            ]

    return np.array(positions, dtype='f4'), np.array(indices, dtype='i4')
