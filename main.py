import numpy as np
import open3d as o3d
import utils
P = np.load('calibration_matrices\\0_P5.npy')
depth_pcd = np.load('depth_maps\\pcd_0.npy')
depth_map = np.load('depth_maps\\depth_map_0.npy')

pcd = []

# Depth camera parameters:
FX_DEPTH = 1.0/P[0][0]
FY_DEPTH = 1.0/P[1][1]
S = -P[0][2]*FY_DEPTH*FX_DEPTH
CY_DEPTH = -P[1][2]*FY_DEPTH
CX_DEPTH = -(P[0][2]*FY_DEPTH*FX_DEPTH-S*CY_DEPTH)/FY_DEPTH

# compute point cloud:
pcd = []
height, width = depth_map.shape
scalar = 0.00001
for i in range(height):
    for j in range(width):
        z = scalar*depth_map[i][j]
        x = (j - CX_DEPTH) * z / FX_DEPTH
        y = (i - CY_DEPTH) * z / FY_DEPTH
        if z < 100*scalar:
            pcd.append(np.array([x, -y, z]))

pcd_o3d = o3d.geometry.PointCloud()
pcd_o3d.points = o3d.utility.Vector3dVector(pcd)

o3d.visualization.draw_geometries([pcd_o3d])