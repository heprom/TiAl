import h5py
from matplotlib import pyplot as plt, cm

f = h5py.File('G2_100_check_euler_rotation.dream3d')
phi1_orig = f['DataContainers']['EbsdDataContainer']['CellData']['EulerAnglesOrig'][0][:, :, 0]
phi1 = f['DataContainers']['EbsdDataContainer']['CellData']['EulerAngles'][0][:, :, 0]
print(phi1.shape)
plt.imshow((phi1_orig - phi1), interpolation='nearest', vmin=0, vmax=360)
plt.colorbar()
plt.show()