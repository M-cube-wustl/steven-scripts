from matplotlib.colors import Normalize
import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import norm

plt.rcParams['axes.unicode_minus'] = False
plt.rcParams.update({'font.size': 20})

four_pi_e0 = 0.0006945 #e^2/eV/m*10^-12
xlen = 620
ylen = 650
zlen = 890
ca_c = 0.75

zr_dir = [[0.918655, 0.511968, 0.034365],
    [0.581345, 0.011968, 0.465635], [0.581345, 0.011968, 0.034365],
    [0.918655, 0.511968, 0.465635], [0.918655 - 1, 0.511968, 0.034365],
    [0.581345, 0.011968 + 1, 0.465635], [0.581345, 0.011968 + 1, 0.034365],
    [0.918655 -1, 0.511968, 0.465635]]
#zr_dir = [[1.0, 0.5, 0.0], [0.5, 0.0, 0.5], [0.5, 0.0, 0.0],
#    [1.0, 0.5, 0.5], [0.0, 0.5, 0.0], [0.5, 1.0, 0.5], [0.5, 1.0, 0.0],
#    [0.0, 0.5, 0.5]]

zr_cart = [np.asarray([int(i[0]*xlen), int(i[1]*ylen),
    int(i[2]*zlen)]) for i in zr_dir]
print(zr_cart)

def pot(x,y,z,cat_pos):
    pos = np.asarray([x,y,z])
    return sum([4.0/(four_pi_e0 * norm(i - pos)) for i in cat_pos])

cell = np.ndarray((xlen,ylen,zlen)) #6.243, 6.547, 8.851
for x in range(xlen):
    for y in range(ylen):
        cell[x,y,int(zlen*ca_c)] = pot(x,y,int(zlen*ca_c), zr_cart)
        
plt.imshow(np.asarray(cell[:,:,int(zlen*ca_c)]).T, aspect='auto', cmap='jet', interpolation='nearest',
    norm=Normalize(vmin=72, vmax=92, clip=True))  #100, 110 for zr plane
plt.xlabel('Location (pm)')
#72,92 for ca plane
cbar = plt.colorbar()
cbar.set_label('Zr potential (V)')
plt.tight_layout()
plt.show()