import h5py
import numpy as np
from matplotlib import pyplot as plt, cm

#f = h5py.File('G2_TRIBEAM.dream3d')
#ipf = f['DataContainers']['ImageDataContainer']['CellData']['IPFColor']
f = h5py.File('../G2.dream3d')
ipf = f['DataContainers']['TribeamDataContainer']['CellData']['IPFColor']
print(ipf.shape)
pixel_size = 1.5  # micron
slice_nb = (12 + 180) / pixel_size  # slice is at Z = 12 microns
ipf_slice = ipf[slice_nb, :, :, :].astype(np.float32) / 255
print(ipf_slice.shape, ipf_slice.dtype)
plt.imshow(np.transpose(ipf_slice, (1, 0, 2)))
plt.imsave('ipf_slice.png', np.transpose(ipf_slice, (1, 0, 2)))
plt.show()
f.close()
