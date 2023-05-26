import os
import numpy as np
from stl import mesh

os.chdir(os.path.dirname(os.path.abspath(__file__)))
# Load the STL file
my_mesh = mesh.Mesh.from_file('../tests/ikea.stl')


def angle(v1, v2):
    # Returns the angle in radians between vectors 'v1' and 'v2'
    cos_ang = np.dot(v1, v2)
    sin_ang = np.linalg.norm(np.cross(v1, v2))
    return np.arctan2(sin_ang, cos_ang)


def are_adjacent(face1, face2):
    """Returns True if the faces share exactly two vertices, False otherwise"""
    shared_vertices = np.isin(face1, face2).sum()
    return shared_vertices == 2


sharp_angle_threshold = np.radians(90)
for i, normal in enumerate(my_mesh.normals):
    for j in range(i + 1, len(my_mesh.normals)):
        if are_adjacent(my_mesh.vectors[i], my_mesh.vectors[j]):
            if angle(normal, my_mesh.normals[j]) > sharp_angle_threshold:
                # print(f"The angle is {angle(normal, my_mesh.normals[j])}")
                print(f"Sharp edge found between faces {i} and {j}")
