import pickle as pkl
import pandas as pd
import utils
import open3d as o3d
import numpy as np
#import convert_depth

pcd = np.load('depth_maps\\pcd_3.npy')
box = pd.read_pickle('aiodrive_boxes_mini\\box\\000003.pkl')

lidar_boxes = [box['lidar'][0]]
geometries = []
for entry in lidar_boxes:
    points = np.array(entry)
    line_set = utils.createBox(points)

    pcd_box = o3d.geometry.PointCloud()  # create point cloud object
    pcd_box.points = o3d.utility.Vector3dVector(points)  # set pcd_np as the point cloud points
    geometries.append(pcd_box)
    geometries.append(line_set)
    print(pcd_box.get_center())
pcd_o3d = o3d.geometry.PointCloud()  # create point cloud object
pcd_o3d.points = o3d.utility.Vector3dVector(pcd)  # set pcd_np as the point cloud points
R = pcd_o3d.get_rotation_matrix_from_xyz((1.0 * np.pi, 0.0 * np.pi,0.0 * np.pi))
pcd_o3d = pcd_o3d.rotate(R, center=pcd_o3d.get_center())
pcd_o3d = pcd_o3d.translate(np.array([-470.0,-125.0,-30.0]))
pcd_o3d = pcd_o3d.scale(0.05,[3.65186891,258.10845724,-1.85348926])
#o3d.visualization.draw_geometries([pcd_o3d,pcd_box,line_set,axis_lines])

viewer = o3d.visualization.Visualizer()
viewer.create_window()
geometries.append(pcd_o3d)

for geometry in geometries:
    viewer.add_geometry(geometry)
opt = viewer.get_render_option()
opt.show_coordinate_frame = True
viewer.run()
viewer.destroy_window()