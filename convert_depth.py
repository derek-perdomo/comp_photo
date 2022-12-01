import imageio.v3 as iio
import numpy as np
import matplotlib.pyplot as plt
import open3d as o3d
import copy
import utils
import cv2

# Read depth image:
depth_image = iio.imread('aiodrive_depth_mini\\depth_0\\000000.png')
depth_map = np.full((depth_image.shape[0],depth_image.shape[1]), 0)
height = depth_image.shape[0]
width = depth_image.shape[1]
pcd = []
for i in range(height):
    for j in range(width):
        pixel = depth_image[i][j]
        norm = float(pixel[0]) + float(pixel[1])*256.0 + float(pixel[2])*256.0*256.0
        depth = 1000.0*(norm/(256.0*256.0*256.0 - 1.0))
        depth_map[i][j] = depth
        if depth < 100:
            pcd.append(np.array([-i, j, depth]))

pcd_o3d = o3d.geometry.PointCloud()  # create point cloud object
pcd_o3d.points = o3d.utility.Vector3dVector(pcd)  # set pcd_np as the point cloud points
o3d.visualization.draw_geometries([pcd_o3d])