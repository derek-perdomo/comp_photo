import numpy as np
import math
import open3d as o3d
def rotate_z (zrot):
    return np.array(((math.cos(zrot), -math.sin(zrot), 0),
                    (math.sin(zrot), math.cos(zrot), 0),
                    (0, 0, 1)))

def rotate_x (xrot):
    return np.array(((1, 0, 0),
                     (math.cos(xrot), -math.sin(xrot), 0),
                     (math.sin(xrot), math.cos(xrot), 1)))

def rotate_y (yrot):
    return np.array(((math.cos(yrot), 0, math.sin(yrot)),
                     (0, 1, 0),
                     (-math.sin(yrot), 0, math.cos(yrot))))

def expandPMatrix(P):
    new_P = np.zeros((4, 4))
    for i in range(3):
        for j in range(4):
            new_P[i][j] = P[i][j]
    new_P[3][3] = 1
    return new_P

def createBox(points):
    lines = [
        [0,1],
        [1,2],
        [2,3],
        [3,0],
        [4,5],
        [5,6],
        [6,7],
        [7,4],
        [0,4],
        [1,5],
        [2,6],
        [3,7]
    ]
    colors_pcd = [[0, 0, 0] for i in range(len(lines))]
    line_set_pcd = o3d.geometry.LineSet(
        points=o3d.utility.Vector3dVector(points),
        lines=o3d.utility.Vector2iVector(lines),
    )

    line_set_pcd.colors = o3d.utility.Vector3dVector(colors_pcd)
    return line_set_pcd

def draw_axis():
    lines = [
        [0, 1],
        [0, 2],
        [0, 3]
    ]
    points = [np.array([0,0,0]),np.array([100,0,0]),np.array([0,100,0]),np.array([0,0,100])]
    colors_pcd = [[255, 0, 0],[0,255,0],[0,0,255]]
    line_set_pcd = o3d.geometry.LineSet(
        points=o3d.utility.Vector3dVector(points),
        lines=o3d.utility.Vector2iVector(lines),
    )

    line_set_pcd.colors = o3d.utility.Vector3dVector(colors_pcd)
    return line_set_pcd