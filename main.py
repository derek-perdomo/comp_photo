import imageio.v3 as iio
import numpy as np
import matplotlib.pyplot as plt
import open3d as o3d
import copy
import utils
import cv2

# Read depth image:
rgb_image = iio.imread('aiodrive_image_mini\\image_0\\000000.png')
depth_image = cv2.imread('aiodrive_depth_mini\\depth_0\\000000.png')

exit(0)
# print properties:
print(f"Image resolution: {depth_image.shape}")
print(f"Data type: {depth_image.dtype}")
print(f"Min value: {np.min(depth_image)}")
print(f"Max value: {np.max(depth_image)}")

center_diff = np.array([0, 0, 0])

# compute point cloud:
pcd = []
height = depth_image.shape[0]
width = depth_image.shape[1]
scalar = float(1000.0 / 255.0)

P0 = [[-5.542562584220e+02, 0.000000000000e+00, -9.600000000000e+02, -4.298717405335e+03],
      [-4.408728476930e-14, 5.542562584220e+02, -3.600000000000e+02, -1.612019027001e+03],
      [-1.224646799147e-16, 0.000000000000e+00, -1.000000000000e+00, -4.477830630557e+00]]

P1 = [[-9.600000000000e+02, 0.000000000000e+00, 5.542562584220e+02, 2.476530171003e+02],
      [-3.600000000000e+02, 5.542562584220e+02, 2.204364238465e-14, -3.724764131287e+02],
      [-1.000000000000e+00, 0.000000000000e+00, 6.123233995737e-17, -1.034656703135e+00]]

P2 = [[5.542562584220e+02, 0.000000000000e+00, 9.600000000000e+02, 0.000000000000e+00],
      [0.000000000000e+00, 5.542562584220e+02, 3.600000000000e+02, 0.000000000000e+00],
      [0.000000000000e+00, 0.000000000000e+00, 1.000000000000e+00, 0.000000000000e+00]]

P3 = [[5.542562584220e+02, 0.000000000000e+00, 9.600000000000e+02, -4.434077734343e+02],
      [0.000000000000e+00, 5.542562584220e+02, 3.600000000000e+02, 0.000000000000e+00],
      [0.000000000000e+00, 0.000000000000e+00, 1.000000000000e+00, 0.000000000000e+00]]

P4 = [[9.600000000000e+02, 0.000000000000e+00, -5.542562584220e+02, -2.234212808587e+03],
      [3.600000000000e+02, 5.542562584220e+02, 2.204364238465e-14, -3.724768749498e+02],
      [1.000000000000e+00, 0.000000000000e+00, 6.123233995737e-17, -1.034657985972e+00]]

P5 = [[5.542562584220e+02, 9.600000000000e+02, 5.878304635907e-14, 2.398603752136e+04],
      [0.000000000000e+00, 9.600000000000e+02, -5.542562584220e+02, 2.398603752136e+04],
      [0.000000000000e+00, 1.000000000000e+00, 6.123233995737e-17, 2.498545575142e+01]]

FX_DEPTH = P3[0][0]
FY_DEPTH = P3[1][1]
CX_DEPTH = P3[0][2]
CY_DEPTH = P3[1][2]

for i in range(height):
    for j in range(width):
        z = int(scalar * depth_image[i][j])
        x = (j - CX_DEPTH) * z / FX_DEPTH
        y = (i - CY_DEPTH) * z / FY_DEPTH
        pcd.append(np.array([x, -y, z]) - center_diff)

pcd_o3d = o3d.geometry.PointCloud()  # create point cloud object
pcd_o3d.points = o3d.utility.Vector3dVector(pcd)  # set pcd_np as the point cloud points
o3d.visualization.draw_geometries([pcd_o3d])
