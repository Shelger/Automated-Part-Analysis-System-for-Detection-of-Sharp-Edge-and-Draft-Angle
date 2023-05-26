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
    # Returns the angle in radians between vectors 'v1' and 'v2'
    cos_ang = np.dot(v1, v2)
    sin_ang = np.linalg.norm(np.cross(v1, v2))
    return np.arctan2(sin_ang, cos_ang)


def are_adjacent(face1, face2):
    """Returns True if the faces share exactly two vertices, False otherwise"""
    shared_vertices = sum(any(np.array_equal(v, w) for w in face2) for v in face1)
    return shared_vertices == 2


sharp_angle_threshold = np.radians(90)
highlight_faces = []
for i, normal in enumerate(my_mesh.normals):
    for j in range(i + 1, len(my_mesh.normals)):
        if are_adjacent(my_mesh.vectors[i], my_mesh.vectors[j]):
            # print(f"point between faces {my_mesh.vectors[i]} and  {my_mesh.vectors[j]}")
            if angle(normal, my_mesh.normals[j]) >= sharp_angle_threshold:
                print(f"The angle is {np.degrees(angle(normal, my_mesh.normals[j]))}")
                print(f"Sharp edge found between faces {i} and {j}")
                if i not in highlight_faces:
                    highlight_faces.append(i)
visualize_mesh(my_mesh, highlight_faces)
