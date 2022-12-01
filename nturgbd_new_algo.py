import imageio.v3 as iio
import numpy as np
import matplotlib.pyplot as plt
import open3d as o3d
import copy
import utils_nturgbd

un = utils_nturgbd.NTURGBD_Setup()
# Globals
scalar = 1
joint_start = 0
joint_end   = 24
center_diff =  np.array([0.07229,-0.00293,-0.05065]) #np.array([0.0646,-0.00564,-0.11755])
frame_num = 1
skeleton_npy_file = '..\\datasets\\NTURGB-D\\data\\skeletons_npy\\S001C001P001R001A001.skeleton.npy'

setup_num = 1
camera_num = 1

# Execution
skel = np.load(skeleton_npy_file, allow_pickle=True).item(0)
skel_body = skel['skel_body0'][frame_num-1]
depth_body = skel['depth_body0'][frame_num-1]

joint_x = [scalar*skel_body[joint][0] for joint in range(joint_start,joint_end+1)]
joint_y = [scalar*skel_body[joint][1] for joint in range(joint_start,joint_end+1)]
joint_z = [scalar*skel_body[joint][2] for joint in range(joint_start,joint_end+1)]
joint_pcd = [[joint_x[joint],joint_y[joint],joint_z[joint]] for joint in range(joint_start,joint_end+1)]
depth_x = [depth_body[joint][0] for joint in range(joint_start,joint_end+1)]
depth_y = [depth_body[joint][1] for joint in range(joint_start,joint_end+1)]

depth_x_proj = []
depth_y_proj = []
depth_z_proj = []

# Read depth image:
depth_image = iio.imread('..\\datasets\\NTURGB-D\\data\\S001C001P001R001A001\\MDepth-00000001.png')

# print properties:
print(f"Image resolution: {depth_image.shape}")
print(f"Data type: {depth_image.dtype}")
print(f"Min value: {np.min(depth_image)}")
print(f"Max value: {np.max(depth_image)}")

depth_grayscale = np.array(255 * depth_image / 0x0fff,
                            dtype=np.uint8)
iio.imwrite('output/grayscale.png', depth_grayscale)

# Depth camera parameters:
FX_DEPTH = 365.60
FY_DEPTH = 365.36
CX_DEPTH = 248.82
CY_DEPTH = 208.63


# compute point cloud:
pcd = []
height, width = depth_image.shape

for joint in range(len(depth_x)):
    i = int(np.ceil(depth_y[joint]))
    j = int(np.ceil(depth_x[joint]))
    z = depth_image[i][j]/1000
    x = (j - CX_DEPTH) * z / FX_DEPTH
    y = (i - CY_DEPTH) * z / FY_DEPTH
    pcd.append(np.array([x, -y, z]) - center_diff)

pcd_o3d = o3d.geometry.PointCloud()  # create point cloud object
pcd_o3d.points = o3d.utility.Vector3dVector(pcd)  # set pcd_np as the point cloud points

#Rotate

#R = un.camera_id_rot_matrix_info[1]
#pcd_o3d = pcd_o3d.rotate(R, center=pcd_o3d.get_center())
#R = pcd_o3d.get_rotation_matrix_from_xyz((0.0 * np.pi, 0.25 * np.pi,0.5 * np.pi))
#pcd_o3d = pcd_o3d.rotate(R, center=pcd_o3d.get_center())
joint_o3d = o3d.geometry.PointCloud()  # create point cloud object
joint_o3d.points = o3d.utility.Vector3dVector(joint_pcd)  # set pcd_np as the point cloud points

depth_cloud = np.asarray(pcd_o3d.points)
joint_cloud = np.asarray(joint_o3d.points)

pcd_center = pcd_o3d.get_center()
joint_center = joint_o3d.get_center()
center_diff = pcd_center-joint_center
# Visualize:
#o3d.visualization.draw_geometries([pcd_o3d])
#o3d.visualization.draw_geometries([joint_o3d])
pcd_o3d.paint_uniform_color([1, 0, 0])
joint_o3d.paint_uniform_color([0, 0, 1])

lines = [
    [3, 2],
    [2, 20],
    [20, 4],
    [20, 8],
    [20, 1],
    [8, 9],
    [9, 10],
    [4, 5],
    [5, 6],
    [1, 0],
    [0, 16],
    [0, 12],
    [16, 17],
    [17, 18],
    [18, 19],
    [12, 13],
    [13, 14],
    [14, 15]
]
colors_pcd = [[1, 0, 0] for i in range(len(lines))]
line_set_pcd = o3d.geometry.LineSet(
    points=o3d.utility.Vector3dVector(depth_cloud),
    lines=o3d.utility.Vector2iVector(lines),
)

colors_joints = [[0, 0, 1] for i in range(len(lines))]
line_set_joints = o3d.geometry.LineSet(
    points=o3d.utility.Vector3dVector(joint_cloud),
    lines=o3d.utility.Vector2iVector(lines),
)

line_set_pcd.colors = o3d.utility.Vector3dVector(colors_pcd)
line_set_joints.colors = o3d.utility.Vector3dVector(colors_joints)

o3d.visualization.draw_geometries([pcd_o3d, joint_o3d, line_set_pcd, line_set_joints])

