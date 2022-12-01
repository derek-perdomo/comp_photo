import imageio.v3 as iio
import numpy as np
import matplotlib.pyplot as plt
import open3d as o3d
import copy
import utils
import cv2
import glob

# Read depth image:
depth_images = [iio.imread(file) for file in glob.glob('aiodrive_depth_mini\\depth_0\\00000*.png')]
x=0
for depth_image in depth_images:
    height = depth_image.shape[0]
    width = depth_image.shape[1]
    pcd = []
    for i in range(height):
        for j in range(width):
            pixel = depth_image[i][j]
            norm = float(pixel[0]) + float(pixel[1])*256.0 + float(pixel[2])*256.0*256.0
            depth = 1000.0*(norm/(256.0*256.0*256.0 - 1.0))
            if depth < 100:
                pcd.append(np.array([-i, j, depth]))
    np.save('depth_maps\\'+str(x)+'.npy',np.array(pcd))
    print('saved file')
    x=x+1
#pcd_o3d = o3d.geometry.PointCloud()  # create point cloud object
#pcd_o3d.points = o3d.utility.Vector3dVector(pcd)  # set pcd_np as the point cloud points
#o3d.visualization.draw_geometries([pcd_o3d])