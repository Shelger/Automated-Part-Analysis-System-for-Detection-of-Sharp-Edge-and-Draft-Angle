import os
import numpy as np
from stl import mesh

os.chdir(os.path.dirname(os.path.abspath(__file__)))
# Load the STL file
my_mesh = mesh.Mesh.from_file('../tests/ikea.stl')


def angle(v1, v2):
    """Returns the angle in radians between vectors 'v1' and 'v2'"""
    cos_ang = np.dot(v1, v2)
    sin_ang = np.linalg.norm(np.cross(v1, v2))
    return np.arctan2(sin_ang, cos_ang)


# Set the direction of pull is the positive direction of axis y
# Thus no vector can be perpendicular to the axis y
def draft_angle(normal):
    """Returns the draft angle in radians for a face with the given normal vector"""
    y_vector = np.array([0, 1, 0])
    return angle(normal, y_vector)


draft_angle_criteria = np.radians(90)
for i, normal in enumerate(my_mesh.normals):
    draft_ang = draft_angle(normal)
    if draft_ang == draft_angle_criteria:  # Assuming negative angles are undercuts
        print(f"Undercut (negative draft angle) found on face {i} with angle {np.degrees(draft_ang)} degrees")