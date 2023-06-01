import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from stl import mesh

os.chdir(os.path.dirname(os.path.abspath(__file__)))
# Load the STL file
my_mesh = mesh.Mesh.from_file('../tests/LinearMotionGuide.stl')


def visualize_edges(mesh, highlight_edges):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    lines = []
    for v in mesh.vectors:
        for i in range(3):
            lines.append(v[[i, (i+1)%3], :])
    line_collection = Line3DCollection(lines, linewidths=0.3, colors='b', alpha=0.1)

    highlight_lines = []
    for edge in highlight_edges:
        highlight_lines.append(edge)
    highlight_line_collection = Line3DCollection(highlight_lines, linewidths=0.9, colors='r', alpha=1.0)

    ax.add_collection3d(line_collection)
    ax.add_collection3d(highlight_line_collection)

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
    face1_set = set(map(tuple, face1))
    face2_set = set(map(tuple, face2))
    shared_vertices = face1_set & face2_set
    if len(shared_vertices) == 2:
        return np.array(list(shared_vertices))
    else:
        return None


sharp_angle_threshold = np.radians(90)
highlight_edges = []
for i, normal in enumerate(my_mesh.normals):
    for j in range(i + 1, len(my_mesh.normals)):
        shared_vertices = are_adjacent(my_mesh.vectors[i], my_mesh.vectors[j])
        if shared_vertices is not None:
            # print(shared_vertices)
            angle_between_normals = angle(normal, my_mesh.normals[j])
            if angle_between_normals >= sharp_angle_threshold:
                highlight_edges.append(shared_vertices)
print(len(highlight_edges))
visualize_edges(my_mesh, highlight_edges)
