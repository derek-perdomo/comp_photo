
import numpy as np
import utils

"""
Write a function that returns the camera matrix, camera intrinsic matrix, and camera extrinsic matrix

Inputs: setup ID, Camera ID
Outputs: Camera Matrix, Camera Intrinsic Matrix, Camera Extrinsic Matrix

"""


class NTURGBD_Setup:

    def __init__(self):
        self.d_scalar = 150*1.8
        self.pxToMetre = 0.001

        # Info obtained from 'A New Model of RGBD Camera Calibration Based on 3-D Control Field' by Zhang et al.
        self.depth_camera_info = {
            'fx': 365.60,
            'fy': 365.36,
            'cx': 248.82,
            'cy': 208.63,
            'k1': 0.07923,
            'k2': -0.14888,
            'p1': -0.00016,
            'p2': -0.00002
        }

        self.rgb_camera_info = {
            'fx': 1055.47,
            'fy': 1055.15,
            'cx': 940.58,
            'cy': 524.74,
            'k1': 0.04426,
            'k2': 0.03956,
            'p1': -0.00006,
            'p2': -0.00064
        }

        # Setup Table with Measurements in meters
        # Keys = Setup Number
        self.setup_info = {
            1: {
                'height': 1.7,
                'distance': 3.5
            },

            2: {
                'height': 1.7,
                'distance': 2.5
            },

            3: {
                'height': 1.4,
                'distance': 2.5
            },

            4: {
                'height': 1.2,
                'distance': 3.0
            },

            5: {
                'height': 1.2,
                'distance': 3.0
            },

            6: {
                'height': 0.8,
                'distance': 3.5
            },

            7: {
                'height': 0.5,
                'distance': 4.5
            },

            8: {
                'height': 1.4,
                'distance': 3.5
            },

            9: {
                'height': 0.8,
                'distance': 2.0
            },

            10: {
                'height': 1.8,
                'distance': 3.0
            },

            11: {
                'height': 1.9,
                'distance': 3.0
            },

            12: {
                'height': 2.0,
                'distance': 3.0
            },

            13: {
                'height': 2.1,
                'distance': 3.0
            },

            14: {
                'height': 2.2,
                'distance': 3.0
            },

            15: {
                'height': 2.3,
                'distance': 3.5
            },

            16: {
                'height': 2.7,
                'distance': 3.5
            },

            17: {
                'height': 2.5,
                'distance': 3.0
            }

        }

        # Camera Id Rotation Table
        # Keys = Camera Id
        # Values = (radian degrees)
        self.camera_id_info = {
            1: np.pi / 2,  # -45 degrees
            2: 0,
            3: -np.pi / 2  # 45 degrees
        }

        # Depth Camera Intrinsic Matrix
        self.depth_camera_intrinsic_matrix = np.array(((self.depth_camera_info['fx'], 0, self.depth_camera_info['cx']),
                                                        (0, self.depth_camera_info['fy'], self.depth_camera_info['cy']),
                                                        (0, 0, 1)))

        # RGB Camera Intrinsic Matrix
        self.rgb_camera_intrinsic_matrix = np.array(((self.rgb_camera_info['fx'], 0, self.rgb_camera_info['cx']),
                                                       (0, self.rgb_camera_info['fy'], self.rgb_camera_info['cy']),
                                                       (0, 0, 1)))

        # Camera Id Rotation MatrixTable
        # Keys = Camera Id
        self.camera_id_rot_matrix_info = {
            1: utils.rotate_z(self.camera_id_info[1]),
            2: utils.rotate_z(self.camera_id_info[2]),
            3: utils.rotate_z(self.camera_id_info[3]),
        }

        # Setup Id Translation Matrix Table
        # Keys = Setup ID
        # Values = Camera Id Translation Matrix Table (Keys = Camera ID)
        self.camera_id_translation_matrix = {}

        # Camera Extrinsic Matrix
        # Keys = Setup ID
        # Values = Camera Id Translation Matrix Table (Keys = Camera ID)
        self.camera_extrinsic_matrix = {}
        self.camera_depth_p_matrix = {}
        self.camera_rgb_p_matrix = {}

        for setup,parameters in self.setup_info.items():
            distance = parameters['distance']
            height = parameters['height']
            camera_t_dict = {}
            camera_e_dict = {}
            camera_depth_p_dict = {}
            camera_rgb_p_dict = {}
            for camera, theta in self.camera_id_info.items():
                x = distance * np.cos(theta)
                y = distance * np.sin(theta)
                z = height
                t = np.array([[x],[y],[z]])
                R = self.camera_id_rot_matrix_info[camera]
                camera_t_dict[camera] = t
                extrinsic_mat = np.hstack((R,t))
                camera_e_dict[camera] = extrinsic_mat
                #camera_depth_p_dict[camera] = self.get_P(self.depth_camera_intrinsic_matrix, extrinsic_mat)
            self.camera_id_translation_matrix[setup] = camera_t_dict
            self.camera_extrinsic_matrix[setup] = camera_e_dict
            self.camera_depth_p_matrix[setup] = camera_depth_p_dict
            self.camera_rgb_p_matrix[setup] = camera_rgb_p_dict

    def convert_from_uvd(self, u, v, d):
        d *= self.pxToMetre * self.d_scalar
        x_over_z = (self.depth_camera_info['cx'] - u) / self.depth_camera_info['fx']
        y_over_z = (self.depth_camera_info['cy'] - v) / self.depth_camera_info['fy']
        z = d / np.sqrt(1. + x_over_z ** 2 + y_over_z ** 2)
        x = x_over_z * z
        y = y_over_z * z
        return x, y, z

    def get_P(self,intrinsics,extrinsics):
        extended_intrinsics = intrinsics
        extended_extrinsics = extrinsics
        extended_intrinsics = np.append(extended_intrinsics,[0,0,0,1])
        extended_intrinsics = np.append(extended_intrinsics, [[0],[0],[0],[1]],1)
        extended_extrinsics = np.append(extended_extrinsics,[0,0,0,1])
        P = np.matmul(extended_intrinsics,extended_extrinsics)
        return P