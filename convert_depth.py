import imageio.v3 as iio
import numpy as np
import glob

# Read depth image:
depth_images = [iio.imread(file) for file in glob.glob('aiodrive_depth_mini\\depth_0\\00000*.png')]
x=0
scalar= 2.0
for depth_image in depth_images:
    print(x)
    depth_map = np.full((720,1920),0)
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
                pcd.append(np.multiply(np.array([j, i, depth]),np.array([0.65, 0.85, 2.])))
    np.save('depth_maps\\pcd_'+str(x)+'.npy',np.array(pcd))
    np.save('depth_maps\\depth_map_' + str(x) + '.npy', depth_map)
    x=x+1