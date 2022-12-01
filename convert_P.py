import numpy as np
import glob

files = [open(file, "r").readlines() for file in glob.glob('aiodrive_calibration_mini\\calib\\*.txt')]
x = 0
for file in files:
    P0 = file[0][4:-1].split(' ')
    P1 = file[1][4:-1].split(' ')
    P2 = file[2][4:-1].split(' ')
    P3 = file[3][4:-1].split(' ')
    P4 = file[4][4:-1].split(' ')
    P5 = file[5][4:-1].split(' ')

    for i in range(12):
        P0[i] = float(P0[i])
        P1[i] = float(P1[i])
        P2[i] = float(P2[i])
        P3[i] = float(P3[i])
        P4[i] = float(P4[i])
        P5[i] = float(P5[i])

    P0 = np.array(P0).reshape((3,4))
    P1 = np.array(P1).reshape((3,4))
    P2 = np.array(P2).reshape((3,4))
    P3 = np.array(P3).reshape((3,4))
    P4 = np.array(P4).reshape((3,4))
    P5 = np.array(P5).reshape((3,4))

    np.save('calibration_matrices\\'+str(x)+'_P0.npy',P0)
    np.save('calibration_matrices\\'+str(x)+'_P1.npy',P1)
    np.save('calibration_matrices\\'+str(x)+'_P2.npy',P2)
    np.save('calibration_matrices\\'+str(x)+'_P3.npy',P3)
    np.save('calibration_matrices\\'+str(x)+'_P4.npy',P4)
    np.save('calibration_matrices\\'+str(x)+'_P5.npy',P5)
    x=x+1