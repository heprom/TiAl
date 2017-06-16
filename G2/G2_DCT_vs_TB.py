import h5py
import numpy as np
from math import pi
from pymicro.crystal.microstructure import Orientation

"""
# read the transformation outputed by dream3d
f = h5py.File('G2_fused_check.dream3d')
trans = f['DataContainers']['DctDataContainer']['Transformation']['SampleTransformation'][0]
print(trans)
R = trans[:3, :3]
print(180/pi*Orientation.misorientation_angle_from_delta(R))
cube = Orientation.cube()
print(Orientation.misorientation_axis_from_delta(R))
f.close()
"""
f = h5py.File('G2.dream3d')
euler_DCT = f['DataContainers']['DctDataContainer']['CellFeatureMatrix']['AvgEuler']
euler_TB = f['DataContainers']['TribeamDataContainer']['CellFeatureData']['AvgEulerAngles']
print(euler_DCT.shape)
print(euler_TB.shape)

pairs = [[3, 6], [9, 13], [41, 52], [48, 81], [74, 71]]
i = 3
gid_DCT = pairs[i][0]
gid_TB = pairs[i][1]
print('euler_DCT: {0:s}'.format(euler_DCT[gid_DCT]))
print('euler_TB: {0:s}'.format(180/pi*euler_TB[gid_TB]))
o_DCT = Orientation.from_euler(euler_DCT[0])
o_TB = Orientation.from_euler(180/pi*euler_TB[gid_TB])
print(o_DCT.disorientation(o_TB))
f.close()
'''

import sys
#sys.path.append('/Users/pollockgroup/Documents/Python')
print(sys.path)

from crystallography.tsl import OimScan
# write DCT and TB slices as .ang files to look at them in OIM
sample = 'G2'
pixel_size = 1.5  # micron
deg2rad = np.pi / 180
f = h5py.File('G2.dream3d')
gids_DCT = f['DataContainers']['DctDataContainer']['CellAttributeMatrix']['GrainIds'][52, :, :, 0]
euler_DCT = f['DataContainers']['DctDataContainer']['CellFeatureMatrix']['AvgEuler']
gids_TB = f['DataContainers']['TribeamDataContainer']['CellData']['FeatureIds'][108, :, :, 0]
euler_TB = f['DataContainers']['TribeamDataContainer']['CellFeatureData']['AvgEulerAngles']
iq_TB = f['DataContainers']['TribeamDataContainer']['CellData']['Image Quality'][108, :, :, 0]
print(gids_DCT.shape)
print(gids_TB.shape)

# read reference EBSD scan
ref_ang_file = 'G2_TRIBEAM/EBSD/ang/TiAl_%s_016_Reg.ang' % sample
ref_scan = OimScan(ref_ang_file)

"""
# dct slice
dct_slice = OimScan.zeros_like(np.empty((gids_DCT.shape[0], gids_DCT.shape[1])), resolution=(pixel_size, pixel_size))
dct_slice.sampleId = 'TiAl_%s_DCT' % sample
# add phases to registered scan if it is empty
if len(dct_slice.phaseList) == 0:
    dct_slice.phaseList.extend(ref_scan.phaseList)
for i in range(gids_DCT.shape[0]):
    for j in range(gids_DCT.shape[1]):
        gid = gids_DCT[i, j]
        if gid == 0:
            dct_slice.euler[i, j, :] = [0., 0., 0.]
        else:
            dct_slice.euler[i, j, 0] = euler_DCT[gid][0] * deg2rad
            dct_slice.euler[i, j, 1] = euler_DCT[gid][1] * deg2rad
            dct_slice.euler[i, j, 2] = euler_DCT[gid][2] * deg2rad
dct_slice.phase = np.ones((gids_DCT.shape[0], gids_DCT.shape[1]))
dct_slice.iq = (dct_slice.euler[:, :, 0] > 0).astype(np.float32)
dct_slice.ci = 2 * dct_slice.iq - 1.
print('writing ang file for dct slice')
dct_slice.writeAng('%s_mid.ang' % dct_slice.sampleId)
"""

# tribeam slice
tb_slice = OimScan.zeros_like(np.empty((gids_TB.shape[0], gids_TB.shape[1])), resolution=(pixel_size, pixel_size))
tb_slice.sampleId = 'TiAl_%s_TB' % sample
# add phases to registered scan if it is empty
if len(tb_slice.phaseList) == 0:
    tb_slice.phaseList.extend(ref_scan.phaseList)
for i in range(gids_TB.shape[0]):
    for j in range(gids_TB.shape[1]):
        gid = gids_TB[i, j]
        if gid == 0:
            tb_slice.euler[i, j, :] = [0., 0., 0.]
        else:
            tb_slice.euler[i, j, 0] = euler_TB[gid][0] #* deg2rad
            tb_slice.euler[i, j, 1] = euler_TB[gid][1] #* deg2rad
            tb_slice.euler[i, j, 2] = euler_TB[gid][2] #* deg2rad
tb_slice.phase = np.ones((gids_TB.shape[0], gids_TB.shape[1]))
tb_slice.iq = iq_TB  #(iq_TB).astype(np.float32)
tb_slice.ci = 2 * (tb_slice.euler[:, :, 0] > 0).astype(np.float32) - 1.
print('writing ang file for ebsd slice')
tb_slice.writeAng('%s_mid.ang' % tb_slice.sampleId)

f.close()

from matplotlib import pyplot as plt
#plt.imshow(dct[:, :, slice], interpolation='nearest')
plt.imshow(tb_slice.euler[:, :, 0].T, interpolation='nearest')
plt.colorbar()
plt.show()
print('done')
'''
