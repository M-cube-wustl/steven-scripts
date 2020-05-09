import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from matplotlib.colors import BoundaryNorm
import matplotlib.patches as patches
import numpy as np
from numpy import polyfit
from scipy.interpolate import spline, interp1d, UnivariateSpline

def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)


def backward_spline(data, range, sp_ord=3):
    xx = np.array([7 - x[0] for x in data])
    sx = np.argsort(xx)
    xx = xx[sx]
    yy = np.array([x[1] for x in data])
    yy = yy[sx]
    return UnivariateSpline(xx, yy, k=sp_ord)


plot_name = 'single'
font_size = 9
conditions = 'low_temp'
plt.close()

# vasp o2 pbesol is -10.2783
E_O2 = -10.2783

kJmol_evsingle = (6.242e21 / 6.022e23)  # converts a kj/mol value to an ev/atom or ev/molecule value
kb_eV = 8.617e-5

# Jc as a function of hole doping, Talantsev et al.
Jc_hole = [(0.156, 0.571), (0.169, 0.940), (0.170, 0.955), (0.173, 1.57), (0.203, 2.57),
           (0.2031, 2.59), (0.207, 2.45), (0.2071, 2.46), (0.212, 2.49), (0.213, 2.491)]

# Hole doping as function of oxygen stoichiometry, liang et al
Hole_stoich = [(6.62, 0.111), (6.67, 0.123), (6.75, 0.133), (6.80, 0.141), (6.86, 0.153), (6.92, 0.165),
               (6.95, 0.174), (6.99, 0.190)]

# Spline function to return stoichiometry (6-7) given hole doping
Hole_spline_stoich = interp1d([x[1] for x in Hole_stoich], [x[0] for x in Hole_stoich],
                              fill_value='extrapolate')
print(Hole_spline_stoich(np.linspace(0.1111, 0.22, 100)))

# I need an array of Jc values as a function of stoichiometry
Jc_stoich = [(float(Hole_spline_stoich(x[0])), x[1]) for x in Jc_hole]

Tc = [(6.63, 62), (6.67, 67), (6.75, 75), (6.80, 84), (6.86, 92), (6.92, 94), (6.95, 93),
      (6.99, 87), (7.00, 85)]
# Tc data digitized from figure 1 in Liang et al. PRB 73 (2006)

H = {  # gas enthalpy correction
    '700': (12.499 + 8.683) * kJmol_evsingle,
    '1100': (26.212 + 8.683) * kJmol_evsingle
}

S = {  # gas entropy correction
    '700': 0.231466 * kJmol_evsingle - kb_eV * np.log(0.2 / 1),
    '1100': 0.246922 * kJmol_evsingle - kb_eV * np.log(0.2 / 1)
}

Temp = {
    'low_temp': '700',
    'high_temp': '1100'
}

# E_oxy = (E_O2 + H[Temp[conditions]] - int(Temp[conditions])*S[Temp[conditions]])/2
E_oxy = E_O2 / 2
print(E_oxy)

conc = [0.25, 0.222, 0.167, 0.125, 0.111, 0.0625, 0.0556]
conc_short = [0.0556, 0.0625, 0.111, 0.25]
concDouble = [0.25, 0.125, 0.0625, 0.056]

BaConf = [.000333, 0.000383, 0.000394]  # Configurational entropy terms
ChainConf = [0.000271, 0.000322, 0.000333]  # assuming vacancies are confined to that sublattice
PlaneConf = [0.000394, 0.000444, 0.000454]

# distCu = [7.61, 15.18/2, 5.42, 3.86, 11.41, 15.18, 11.41]
# distBa = [7.61, 15.18/2, 3.86,  5.42, 11.41, 15.18, 11.41]
dataPrist = {
    'E_248': -384.051,
    'E_248_221': -768.145,
    'E_248_r8': -1536.299,
    'E_248_331': -1728.346,  # from ISIF3 relax
    'E_r8': -680.119,
    'E_221': -340.058,
    'E_441': -1360.276,
    'E_332': -1530.238,
    'E_331': -765.133,
    'E_r2': -340.050,
    'E_2a_3b': -510.083,
    'E_3a_2b': -510.078,
}

dataDoubleChain = [
    (-376.832 + E_oxy - dataPrist['E_248']),
    (-760.914 + E_oxy - dataPrist['E_248_221']),
    (-1529.159 + E_oxy - dataPrist['E_248_r8']),
    (-1721.134 + E_oxy - dataPrist['E_248_331'])]

dataDoubleBa = [
    (-376.267 + E_oxy - dataPrist['E_248']),
    (-760.644 + E_oxy - dataPrist['E_248_221']),
    (-1528.873 + E_oxy - dataPrist['E_248_r8']),
    (-1720.909 + E_oxy - dataPrist['E_248_331'])]  # 248_331_Ba ISIF2 relaxation

dataChain = [
    #    (-333.606+E_oxy-dataPrist['E_221']),
    #    (-1334.451+4*E_oxy-dataPrist['E_441'])/4,
    (-1335.203 + 4 * E_oxy - dataPrist['E_441']) / 4,  # This one is the b-axis closely spaced
    #    (-333.218+E_oxy-dataPrist['E_r2']), #
    (-1504.914 + 4 * E_oxy - dataPrist['E_332']) / 4,  # empty chain
    #    (-1503.959+4*E_oxy-dataPrist['E_332'])/4, #max separation
    #    -503.514+E_oxy-dataPrist['E_2a_3b'],
    -503.658 + E_oxy - dataPrist['E_3a_2b'],
    -673.591 + E_oxy - dataPrist['E_r8'],
    -758.590 + E_oxy - dataPrist['E_331'],
    -1353.763 + E_oxy - dataPrist['E_441'],
    -1523.710 + E_oxy - dataPrist['E_332']
]

dataBa = [
    #	(-333.344+E_oxy-dataPrist['E_221']), #
    (-1333.419 + 4 * E_oxy - dataPrist['E_441']) / 4,  # distrib
    #    (-1333.206+4*E_oxy-dataPrist['E_441'])/4, #
    #    (-332.458+E_oxy - dataPrist['E_r2']), #
    (-1503.492 + 4 * E_oxy - dataPrist['E_332']) / 4,  # max separation
    -503.503 + E_oxy - dataPrist['E_2a_3b'],
    #   -503.472 + E_oxy - dataPrist['E_3a_2b'],
    -673.583 + E_oxy - dataPrist['E_r8'],
    -758.606 + E_oxy - dataPrist['E_331'],
    -1353.756 + E_oxy - dataPrist['E_441'],
    -1523.753 + E_oxy - dataPrist['E_332']
]

dataPlaneA = [
    -1353.233 + E_oxy - dataPrist['E_441'],
    -758.026 + E_oxy - dataPrist['E_331'],
    -332.792 + E_oxy - dataPrist['E_221'],
    -332.016 + E_oxy - dataPrist['E_r2']
]

dataPlaneB = [
    -1523.190 + E_oxy - dataPrist['E_332'],
    -1353.234 + E_oxy - dataPrist['E_441'],
    -758.063 + E_oxy - dataPrist['E_331'],
    -332.810 + E_oxy - dataPrist['E_221'],
    #    -332.049 + E_oxy - dataPrist['E_r2']
]

data = {
    'single': {
        'conc': conc,
        'data_Ba': dataBa,
        'data_Cu': dataChain,
    },
    'double': {
        'conc': concDouble,
        'data_Ba': dataDoubleBa,
        'data_Cu': dataDoubleChain,
    }
}
print(dataChain)
print(dataBa)
print(dataPlaneA)
print(dataPlaneB)
fig, ax1 = plt.subplots(figsize=(3.4, 3))
# ax1 = fig.add_subplot(111)


#BaPlot = ax1.scatter(data[plot_name]['conc'], data[plot_name]['data_Ba'], s=18,
 #                    marker='s', c=(255.0 / 255.0, 74.0 / 255.0, 0.0 / 255.0), lw=0)
#ChainPlot = ax1.scatter(data[plot_name]['conc'], data[plot_name]['data_Cu'], s=19,
 #                       c=(122.0 / 255.0, 155.0 / 255.0, 64.0 / 255.0), lw=0)
#if plot_name == 'single':
    #    PlaneAPlot = ax1.scatter(conc_short, dataPlaneA, marker='v', s=80, c='blue')
#    PlaneBPlot = ax1.scatter(conc_short, dataPlaneB, marker='v', s=20,
 #                            c=(97.0 / 255.0, 64.0 / 255.0, 155.0 / 255.0), lw=0)
#else:
#    PlanePlot = ax1.scatter((), ())
ax1.set_zorder(2)
ax1.patch.set_alpha(0)
ax1.set_xlim(0.0, 0.3)
ax1.set_ylim(0.6, 2.25)
ax1.set_xticks([0, 0.1, 0.2, 0.3])
ax1.tick_params(axis='x', which='major', pad=15)
ax1.set_yticks([1.0, 1.4, 1.8, 2.2])
ax1.set_xlabel('Vacancies per f.u.', fontsize=font_size, labelpad=0.2)
#ax1.set_ylabel(r'Formation Energy (eV/V$_O$)', fontsize=font_size, labelpad=0.1)
ax1.tick_params('both', length=3, width=0.5, labelsize=font_size, right=False, pad=0.8)
ax1.spines['right'].set_color('b')
ax2 = ax1.twiny()
ax2.tick_params(axis='x', length=3, width=0.5, which='major', labelsize=font_size, pad=0.8)
ax2.set_xlim([7 - limit for limit in ax1.get_xlim()])
ax2.set_xlabel(r'Oxygen stoichiometry', fontsize=font_size, labelpad=2.0)
ax2.set_xticks([7 - tick for tick in ax1.get_xticks()])
ax2.set_xticklabels(7 - ax1.get_xticks())
if plot_name == 'single':
    ax3 = ax1.twinx()
    ax4 = ax1.twinx()
    ax4.set_ylim(0, 3)
#    ax4.spines['right'].set_position(('axes', 1.25))
    make_patch_spines_invisible(ax4)
    ax4.spines['right'].set_color('maroon')
    xrange = np.linspace(0, 0.3, 100)
    spline3y = backward_spline(Tc, [0, 0.3], sp_ord=3)
    spline3x = np.linspace(0, 0.3, 100)
    ax3.plot(spline3x, spline3y(spline3x), linewidth=2, color='blue')
    spline4y = backward_spline(Jc_stoich, [-.03, 0.12], sp_ord=3)
    spline4x = np.linspace(-.03, 0.12, 100)
    ax4.plot(spline4x, spline4y(spline4x), linewidth=2, color='maroon')
    ax4.set_xlim(0, 0.3)
    ax3.set_ylabel(r'$T_{c}$ (K)', fontsize=font_size + 2, color='blue', labelpad=0.1)
    ax4.set_ylabel(r'$J_{c}$ (MA$\cdot $cm$^{-2}$)', fontsize=font_size + 2, color='maroon', labelpad=0.01)
    ax3.set_yticks([70, 80, 90])
    ax4.set_yticks([0, 1, 2, 3])
    ax3.tick_params('both', labelsize=font_size, length=3, width=0.5, color='blue',
                    labelcolor='blue', pad=1.2)
    ax4.tick_params('both', labelsize=font_size, length=3, width=0.5, color='maroon',
                    labelcolor='maroon', pad=1.2)
#    ax4.spines['right'].set_visible(False)
#legend = {
#    'single': {
#        'styles': (ChainPlot, BaPlot, PlaneBPlot),
#        'labels': (r'Chain $V_o$', r'Apical $V_o$', r'Planar $V_o$'),  #
#    },
#    'double': {
#        'styles': (ChainPlot, BaPlot),
#        'labels': (r'Chain $V_o$', r'Apical $V_o$')
#    }
#}

#leg = plt.legend(legend[plot_name]['styles'],legend[plot_name]['labels'],fontsize = font_size,
#    scatterpoints=1,loc='lower left', handletextpad=0.01, borderpad=0)
#leg.get_frame().set_alpha(0.5)

# r1 = patches.Rectangle((0.06,0), 0.06, 1.5, color="blue", alpha = 0.1)
# ax1.add_patch(r1)
plt.tight_layout()
#plt.savefig('C:/Users/steve/OneDrive/Pictures/YBCO_PRM/fig1.png', dpi=700, pad_inches=0, format='png')
plt.show()
