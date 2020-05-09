import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
import numpy as np
from scipy import optimize

mode_amp = [-4, -3, -2, -1, 0, 1, 2, 3, 4]

def landau(x, a, b):
    return a * np.power(x, 2) + b * np.power(x, 4)

def get_params(data):
    return optimize.curve_fit(landau, mode_amp, 
    [(p - data[4])/30*1000 for p in data], p0=[-1, 1])
    
def add_points(plots, data, size, mark, color, amps=mode_amp):
    if amps == mode_amp:
        plots.append(ax1.scatter(amps, [(p - data[4])/30*1000 for p in data], s=size, marker=mark,
        c=color, lw=0))
    else:
        plots.append(ax1.scatter(amps, [landau(a, get_params(data)[0][0], 
        get_params(data)[0][1]) for a in amps], s=size, marker=mark, c=color, lw=0))
    return plots
    
 

plt.rcParams['axes.unicode_minus'] = False
plt.rcParams.update({'font.size': 12})

ScSn = [-.22655603E+03, -.22623405E+03, -.22560366E+03, -.22505346E+03,
    -.22483825E+03, -.22505346E+03, -.22560366E+03, -.22623405E+03, -.22655603E+03]
InSn = [-.17559493E+03, -.17539493E+03, -.17502868E+03, -.17472729E+03,
    -.17461345E+03, -.17472729E+03, -.17502868E+03, -.17539493E+03, -.17559493E+03]
EuSn = [-.21826582E+03, -.21809574E+03, -.21775711E+03, -.21745925E+03,
    -.21734308E+03, -.21745925E+03, -.21775711E+03, -.21809574E+03, -.21826582E+03]
YSn = [-.23072262E+03, -.23054778E+03, -.23020421E+03, -.22990531E+03,
    -.22978892E+03, -.22990531E+03, -.23020421E+03, -.23054778E+03, -.23072262E+03]
LaSn = [-.21827580E+03, -.21819283E+03, -.21803302E+03, -.21789424E+03,
    -.21784053E+03, -.21789424E+03, -.21803302E+03, -.21819283E+03, -.21827580E+03]
   
fig = plt.figure(figsize=(3.5,3))
ax1 = fig.add_subplot(111)
ax1.set_xlim((-4.9, 4.9))
ax1.set_ylim((-60, 6))
ax1.tick_params(axis = 'x', which = 'major')
ax1.tick_params(axis = 'y', which = 'major')
ax1.set_xlabel('Relative Amplitude', labelpad=0.2)
ax1.set_xticklabels(['',r'$P6_{3}cm$', '', r'$P6_{3}/mmc$', '', r'$P6_{3}cm$'], fontsize=11)
ax1.set_ylabel('Energy (meV/atom)', labelpad=2)

plots = []
plots = add_points(plots, ScSn, 40, 'D', '#ff804a')
plots = add_points(plots, InSn, 60, 's', '#caf04b', amps=[-2.8,-1.8,-0.8,0.8,1.8,2.8])
plots = add_points(plots, YSn, 60, 'o', '#5fdaff')
plots = add_points(plots, EuSn, 40, 'p', '#5be354', amps=[-2.6,-1.6,-0.6,0.6,1.6,2.6])
plots = add_points(plots, LaSn, 40, 's', '#7262ff')
    
plots.append(ax1.plot(np.linspace(-6,6,num=100), landau(np.linspace(-6, 6, num=100),
    get_params(ScSn)[0][0], get_params(ScSn)[0][1]), color='#ff804a'))
plots.append(ax1.plot(np.linspace(-6,6,num=100), landau(np.linspace(-6, 6, num=100),
    get_params(InSn)[0][0], get_params(InSn)[0][1]), color='#caf04b'))
plots.append(ax1.plot(np.linspace(-6,6,num=100), landau(np.linspace(-6, 6, num=100),
    get_params(YSn)[0][0], get_params(YSn)[0][1]), color='#5fdaff'))
plots.append(ax1.plot(np.linspace(-6,6,num=100), landau(np.linspace(-6, 6, num=100),
    get_params(EuSn)[0][0], get_params(EuSn)[0][1]), color='#5be354'))
plots.append(ax1.plot(np.linspace(-6,6,num=100), landau(np.linspace(-6, 6, num=100),
    get_params(LaSn)[0][0], get_params(LaSn)[0][1]), color='#7262ff'))

plt.legend(plots,['Sc', 'In', 'Y','Eu','La','','','','',''],
#plt.legend(plots,['YSnO$_{2}$N',''],
    handlelength=1, labelspacing=0.3, handletextpad=0.3,
    scatterpoints = 1,loc = 'best', borderpad=0.1, borderaxespad=0.1)
plt.title('Polar Distortion Energy', fontsize=12)
plt.tight_layout()
plt.savefig('C:/Users/steve/Pictures/oxynit_tilt', dpi=400)
plt.show()