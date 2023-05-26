import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from stl import mesh

os.chdir(os.path.dirname(os.path.abspath(__file__)))
# Load the STL file
my_mesh = mesh.Mesh.from_file('../tests/withDraft.stl')


def visualize_mesh(mesh, highlight_faces):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    polygons = []
    color = []
    for i, v in enumerate(mesh.vectors):
        polygons.append(v)
        if i in highlight_faces:
            color.append('r')
        else:
            color.append('b')

    collection = Poly3DCollection(polygons)
    collection.set_facecolor(color)
    ax.add_collection3d(collection)

    scale = mesh.points.flatten()
    ax.auto_scale_xyz(scale, scale, scale)
    plt.show()

def angle(v1, v2):
    """Returns the angle in radians between vectors 'v1' and 'v2'"""
    cos_ang = np.dot(v1, v2)
    sin_ang = np.linalg.norm(np.cross(v1, v2))
    return np.arctan2(sin_ang, cos_ang)


# Set the direction of pull is the positive direction of axis z
# Thus no vector can be perpendicular to the axis z
def draft_angle(normal):
    """Returns the draft angle in radians for a face with the given normal vector"""
    z_vector = np.array([0, 1, 0])
    return angle(normal, z_vector)


draft_angle_criteria = np.radians(90)
highlight_faces = []
for i, normal in enumerate(my_mesh.normals):
    draft_ang = draft_angle(normal)
    if draft_ang == draft_angle_criteria:
        print(f"Draft angle found on face {i} with angle {np.degrees(draft_ang)} degrees")
        highlight_faces.append(i)

print(f"size of {len(my_mesh.normals)}")
visualize_mesh(my_mesh, highlight_faces)