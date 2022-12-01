import imageio.v3 as iio
import numpy as np
import matplotlib.pyplot as plt
import open3d as o3d
import copy
import utils
import cv2
import glob
depth_images = [np.load(file) for file in glob.glob('depth_maps\\*.npy')]

for pcd in depth_images:
    pcd_o3d = o3d.geometry.PointCloud()  # create point cloud object
    pcd_o3d.points = o3d.utility.Vector3dVector(pcd)  # set pcd_np as the point cloud points
    o3d.visualization.draw_geometries([pcd_o3d])
