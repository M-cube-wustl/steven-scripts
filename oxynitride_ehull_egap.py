import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def autolabel(ax, rects, bottom=0):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height() + bottom
        ax.text(rect.get_x() + rect.get_width()/2., 1*height,
            '%.1f' % height,
            ha='center', va='bottom', )

plot_name = 'bar'
bar_type = 'mh'
#A/B uses VIII/VI
#B/X uses VI/IV weighted average (O2N 1.407, ON2 1.433)
#Used average of Mn(III) high and low spin
data = {
'BaAsO2N': {
    'A/B': 3.087,
    'B/X': 0.327,
    'Ehull': 57.6,
    'Egap': 2.91
    },
'BaNbO2N': {
    'A/B': 1.42/0.64,
    'B/X': 0.64/1.407
    },
'BaSnO3': {
    'Egap_hse': 2.43, #jiangang et al 2016
    'me': 0.127,
    'mh': 0.761  #matproj
    },
'CaAsO2N': {
    'A/B': 2.435,
    'B/X': 0.327,
    'Ehull': 81.3,
    'Egap': 2.62
    },
'CeTaON2': {
    'A/B': 1.143/0.64,
    'B/X': 0.64/1.433
    },
'CaMoO2N': {
    'A/B': 1.12/0.61,
    'B/X': 0.61/1.407
    },
'CaNbO2N': {
    'A/B': 1.12/0.68,
    'B/X': 0.68/1.407
    },
'CaSbO2N': {
    'A/B': 1.867,
    'B/X': 0.427,
    'Ehull': 110.2,
    'Egap': 1.67
    },
 'CH3NH3PbI3': {
    'Egap_hse': 1.45,
    'me': 0.135,
    'mh': 0.23
    },
'Cs2AgBiBr6': {
    'Egap_hse': 2.06,
    'me': 0.371,
    'mh': 0.14
    },
#'EuGeO2N': {
#    'Ehull': 37.3,
#    'Egap': 
#    },
'EuSnO2N': {
    'A/B': 1.545,
    'B/X': 0.491,
    'C31': 0.216,
    'C33': -0.302,
    'D11': 14.665,
    'D33': 16.570,
    'Ehull': 0,
    'Egap': 0,
    'Egap_hse': 2.48,
    'me': (.269+.184+.471)/3,
    'mh': 1.69,
    'Polarization': 10.476
    },
'GaAs': {
    'Egap_hse': 1.33 ,
    'me': 0.089,
    'mh': 0.088,
    },
'GdTaON2': {
    'A/B': 1.053/0.64,
    'B/X': 0.64/1.433
    },
'In2O3': {
    'Egap_hse': 2.7,
    'me': 0.198,  #matproj
    'mh': 2.054
    },
'InSnO2N': {
    'A/B': 1.333,
    'B/X': 0.491,
    'C31': -0.122,
    'C33': 0.376,
    'D11': 14.793,
    'D33': 17.744,
    'Ehull': 50.1,
    'Egap': 0.26,
    'Egap_hse': 1.59,
    'me': (.121+.088+.114)/3,
    'mh': 1.43,
    'Polarization': 9.876
    },
 'KBaTeBiO6': {
    'Egap_hse': 1.94,
    'me': 0.278,
    'mh': 0.25
    },
'LaGeO2N': {
    'A/B': 2.189,
    'B/X': 0.377,
    'Ehull': 52.6,
    'Egap': 2.95
    },
'LaSnO2N': {
    'A/B': 1.681,
    'B/X': 0.491,
    'C31': 0.0899,
    'C33': -0.418,
    'D11': 15.654,
    'D33': 17.608,
    'Ehull': 47.8,
    'Egap': 0.93,
    'Egap_hse': 2.20,
    'me': (.300+.204+.675)/3,
    'mh': 2.11,
    'Polarization': 7.111
    },
'LaTiO2N': {
    'A/B': 1.917,
    'B/X': 0.430
    },
'LaVO2N': {
    'A/B': 1.16/0.58,
    'B/X': 0.58/1.407
    },
'LaZrO2N': {
    'A/B': 1.16/0.72,
    'B/X': 0.72/1.407
    },
'LuFeO3': {
    'A/B': 1.635,
    'B/X': 0.433
    },
'LuMnO3': {
    'A/B': 1.595,
    'B/X': 0.444
    },
'NdVO2N': {
    'A/B': 1.109/0.58,
    'B/X': 0.58/1.407
    },
'ScSnO2N': {
    'A/B': 1.261,
    'B/X': 0.491,
    'C31': 0.056,
    'C33': -0.323,
    'D11': 22.175,
    'D33': 17.486,
    'Ehull': 69.8,
    'Egap': 1.82,
    'Egap_hse': 3.28,
    'me': (.269+.230+.735)/3,
    'mh': 3.89,
    'Polarization': 16.776
    },
'SrAsO2N': {
    'A/B': 2.739,
    'B/X': 0.327,
    'Ehull': 46.6,
    'Egap': 2.89
    },
'SrMoO2N': {
    'A/B': 1.26/0.61,
    'B/X': 0.61/1.407
    },
'SrNbO2N': {
    'A/B': 1.26/0.64,
    'B/X': 0.64/1.407
    },
'SrSbO2N': {
    'A/B': 2.1,
    'B/X': 0.427,
    'Ehull': 98.3,
    'Egap': 1.50
    },
'SrTaO2N': {
    'A/B': 1.969,
    'B/X': 0.455,
    },    
'YMnO3': {
    'A/B': 1.664,
    'B/X': 0.444
    },
'YGaO3': {
    'A/B': 1.644,
    'B/X': 0.449
    },
'YGeO2N': {
    'A/B': 1.923,
    'B/X': 0.377,
    'Ehull': 130.9,
    'Egap': 2.91
    },
'YInO3': {
    'A/B': 1.274,
    'B/X': 0.580
    },
'YSiO2N': {
    'A/B': 2.548,
    'B/X': 0.284,
    'Ehull': 7.6,
    'Egap': 3.88
    },
'YSnO2N': {
    'A/B': 1.477,
    'B/X': 0.491,
    'C31': 0.06132,
    'C33': -0.25998,
    'D11': 14.195,
    'D33': 16.493,
    'Ehull': 0,
    'Egap': 1.41,
    'Egap_hse': 2.71,
    'me': (.304+.207+.523)/3,
    'mh': 2.84,
    'Polarization': 11.527
    },
'ZnSnO3': {
    'Egap_hse': 3.02, #Jiangang (rondinelli) 2016
    'me': 0.213,
    'mh': 1.231 #Materials project
    },
}
bar_types = {
    'hse': {
        'autolabel': True,
        'bottom': 0,
        'colors': ['r','r','r','g','g','g','g','b','b','b','b','b'],
        'comps': ['CH3NH3PbI3', 'Cs2AgBiBr6', 'KBaTeBiO6',  'GaAs', 'ZnSnO3', 'In2O3', 'BaSnO3'],
        'formatted_comps': [r'CH$_{3}$NH$_{3}$PbI$_{3}$*', r'Cs$_{2}$AgBiBr$_{6}$', 
            'KBaTeBiO$_{6}$', 'GaAs', r'ZnSnO$_{3}$*', r'In$_{2}$O$_{3}$', r'BaSnO$_{3}$'],
        'data': 'Egap_hse',
        'figsize': [4.3,2.0],
        'label': '$E_{gap}$ (eV)',
        'labelpad': 12,
        'locator': 1,
        'subplots': 1,
        'suptitle': 'Band Gap (HSE06)',
        'ylim': [1,4],
    },
    'hull': {
        'autolabel': True,
        'bottom': -10,
        'colors': ['r','r','r','r','r'],
        'comps': [],
        'formatted_comps': [],
        'data': 'Ehull',
        'figsize': (3,1.6),
        'label': '$E_{hull}$ \n(meV/atom)',
        'labelpad': 2,
        'locator': 50,
        'subplots': 1,
        'suptitle': 'E$_{hull}$ of $A$SnO$_{2}$N',
        'ylim': [-10,100]
    },
    'me': {
        'autolabel': True,
        'bottom': 0,
        'colors': ['r','r','r','g','g','g','g','b','b','b','b','b'],
        'comps': ['CH3NH3PbI3', 'Cs2AgBiBr6', 'KBaTeBiO6',  'GaAs', 'ZnSnO3', 'In2O3', 'BaSnO3'],
        'formatted_comps': [r'CH$_{3}$NH$_{3}$PbI$_{3}$*', r'Cs$_{2}$AgBiBr$_{6}$', 
            'KBaTeBiO$_{6}$', 'GaAs', r'ZnSnO$_{3}$*', r'In$_{2}$O$_{3}$', r'BaSnO$_{3}$'],
        'data': 'me',
        'figsize': [4.3,2.0],
        'label': r'm$_{e}$ (m/m$_{0}$)',
        'labelpad': 1,
        'locator': 0.5,
        'subplots': 1,
        'suptitle': 'Carrier Effective Mass',
        'ylim': [0,0.6]
    },
    'mh': {
        'autolabel': True,
        'bottom': 0,
        'colors': ['r','r','r','g','g','g','g','b','b','b','b','b'],
        'comps': ['CH3NH3PbI3', 'Cs2AgBiBr6', 'KBaTeBiO6', 'GaAs', 'ZnSnO3', 'In2O3', 'BaSnO3'],
        'formatted_comps': [r'CH$_{3}$NH$_{3}$PbI$_{3}$*', r'Cs$_{2}$AgBiBr$_{6}$', 
            'KBaTeBiO$_{6}$', 'GaAs', r'ZnSnO$_{3}$*', r'In$_{2}$O$_{3}$', r'BaSnO$_{3}$'],
        'data': 'mh',
        'figsize': [4.3,2.0],
        'label': r'm$_{h}$ (m/m$_{0}$)',
        'labelpad': 12,
        'locator': 2,
        'subplots': 1,
        'suptitle': '',
        'ylim': [0,5]
    },
    'polarization': {
        'autolabel': True,
        'bottom': 0,
        'colors': ['b','b','b','b','b'],
        'comps': [],
        'formatted_comps': [],
        'data': 'Polarization',
        'figsize': (3.8,1.6),
        'label': 'P ($\mu$C/cm$^{2}$)',
        'locator': 5,
        'subplots': 1,
        'suptitle': 'Polarization of $A$SnO$_{2}$N',
        'ylim': [6,20]
    }
}

#In2O3 hse gap 2.74 walsh et al prb 2009
if plot_name == 'bar':
    bar_dict = bar_types[bar_type]
    #Piezo has same (probably incorrect!) sign as VASP!!!!!
    #Yes, I've double-checked the sign of the InSnO2N piezo results.
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams.update({'font.size': 11})
    plt.rcParams['ytick.major.pad']='1'
    width = 0.6
    sn_comps = bar_dict['comps']
    sn_comps = sn_comps + ['ScSnO2N', 'InSnO2N', 'EuSnO2N', 'YSnO2N', 'LaSnO2N']
    formatted_comps = bar_dict['formatted_comps']
    fig, axes = plt.subplots(bar_dict['subplots'], sharex=True,
        figsize=bar_dict['figsize'])
    if formatted_comps == []:
        formatted_comps = formatted_comps + [r'Sc', r'In', r'Eu', r'Y', r'La']
        axes.axhline(y=0, xmin=0.0, xmax=1.0, color='black', linewidth=1)
    else:
        formatted_comps = formatted_comps + [r'ScSnO$_{2}$N*', r'InSnO$_{2}$N*',
            r'EuSnO$_{2}$N*', r'YSnO$_{2}$N*', r'LaSnO$_{2}$N*']
        plt.xticks(rotation=45, ha="right")
    rects1 = axes.bar([x for x in range(len(sn_comps))], 
        [data[comp][bar_dict['data']] - bar_dict['bottom'] for comp in sn_comps],
        bottom=bar_dict['bottom'], color= bar_dict['colors'],
        width=-width, alpha=0.9, align='center')
    axes.set_xticks(range(len(formatted_comps) + 1))
    axes.set_xticklabels(formatted_comps)
    axes.set_ylabel(bar_dict['label'], labelpad=bar_dict['labelpad'])
    if bar_dict['autolabel']:
        autolabel(axes, rects1, bottom=bar_dict['bottom'])
    fig.suptitle(bar_dict['suptitle'], x=0.58, y=0.99, fontsize=11)
    axes.set_ylim(bar_dict['ylim'])
    axes.yaxis.set_major_locator(ticker.MultipleLocator(bar_dict['locator']))
    plt.tight_layout()
    plt.savefig('C:/Users/steve/Pictures/' + bar_type, dpi=400)
#    axes[1].tick_params(axis='x', which='major', pad=1)
#    axes[1].bar([x for x in range(len(sn_comps))], [data[comp]['me'] for comp in sn_comps], 
#        color=['b' for i in range(5)] + ['r' for i in range(5)], alpha=0.5)
#    axes[1].bar([x for x in range(len(sn_comps))], [data[comp]['mh'] for comp in sn_comps], 
#        color=['b' for i in range(5)] + ['r' for i in range(5)])
#    axes[1].set_ylabel(r'm$^{*}$ (m/m$_{0}$)', labelpad=2)
#        fig.subplots_adjust(hspace=0)
#        for i in range(len(ax1.xaxis.get_major_ticks())):
#            if i%3 == 1:
#                ax1.xaxis.get_major_ticks()[i].set_pad(18)
#            elif i%3 == 2:
#                ax1.xaxis.get_major_ticks()[i].set_pad(30)
                

#    ax2 = axes[1].twinx()
#    ax2.set_xlim([-0.5, len(sn_comps)])
#    rects2 = ax2.bar([x*1.1 - width/2 for x in range(len(sn_comps))], [data[comp]['Egap_hse'] + 1 for comp in sn_comps],
#        bottom=-1, width=width, color='red', alpha=0.7, align='edge')
#    ax2.set_ylabel(r'HSE E$_{Gap}$ (eV)', color='red', labelpad=6)
#    ax2.set_ylim([1,4])
#    ax2.tick_params(color='red', labelcolor='red')
#    ax2.spines['left'].set_color('blue')
#    ax2.spines['right'].set_color('red')
#    ax2.yaxis.set_major_locator(ticker.MultipleLocator(1))

#    rects3 = axes[1].bar([x*1.1 - width/2 for x in range(len(sn_comps))], 
#        [data[comp]['Polarization'] for comp in sn_comps], tick_label=formatted_comps, width=-width,
#        color='green', alpha=0.7, align='edge')
#    axes[1].set_ylabel(r'P ($\mu C/cm^{2}$)', color='green', labelpad=0)
#    axes[1].set_ylim([5,18])
#    axes[1].tick_params('y', color='green', labelcolor='green')    
#    axes[1].yaxis.set_major_locator(ticker.MultipleLocator(5))

#    ax4 = axes[1].twinx()
#    ax4.set_xlim([-0.5, len(sn_comps)])
#    rects4 = ax4.bar([x*1.1 - width/2 for x in range(len(sn_comps))], 
#        [(2*data[comp]['D11'] + data[comp]['D33'])/3 for comp in sn_comps],
#        width=width, color='magenta', alpha=0.7, align='edge')
#    ax4.set_ylabel(r'Permittivity', color='magenta', labelpad=6)
#    ax4.set_ylim([10,25])
#    ax4.tick_params(color='magenta', labelcolor='magenta')
#    ax4.spines['left'].set_color('green')
#    ax4.spines['right'].set_color('magenta')
#    ax4.yaxis.set_major_locator(ticker.MultipleLocator(5))

#rects5 = axes[2].bar([x*1.1 - width/2 for x in range(len(sn_comps))], 
#    [-1 * data[comp]['C31'] for comp in sn_comps], tick_label=formatted_comps, width=-width,
#    color='purple', alpha=0.7, align='edge')
#axes[2].set_ylabel(r'$c_{31}$ ($C/cm^{2}$)', color='purple', labelpad=-10)
#axes[2].set_ylim([-.5, .5])
#axes[2].tick_params('y', color='purple', labelcolor='purple')    
#axes[2].yaxis.set_major_locator(ticker.MultipleLocator(0.5))
#axes[2].axhline()

#ax6 = axes[2].twinx()
#ax6.set_xlim([-0.5, len(sn_comps)])
#rects6 = ax6.bar([x*1.1 - width/2 for x in range(len(sn_comps))], 
#    [-1 *data[comp]['C33'] for comp in sn_comps],
#    width=width, color='deepskyblue', alpha=0.7, align='edge')
#ax6.set_ylabel(r'$c_{33}$ ($C/cm^{2}$)', color='deepskyblue', labelpad=-4)
#ax6.set_ylim([-.5,.5])
#ax6.tick_params(color='deepskyblue', labelcolor='deepskyblue')
#ax6.spines['left'].set_color('purple')
#ax6.spines['right'].set_color('deepskyblue')
#ax6.yaxis.set_major_locator(ticker.MultipleLocator(0.5))
    plt.show()
    
if plot_name == 'scatter':
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams.update({'font.size': 14})
    YSnO2N = ['EuSnO2N', 'InSnO2N', 'LaSnO2N', 'ScSnO2N', 'YSnO2N']
    LuMnO3 = ['LuMnO3', 'YMnO3', 'YGaO3', 'YInO3', 'LuFeO3']
    YSiO2N = ['BaAsO2N', 'CaAsO2N', 'LaGeO2N', 'SrAsO2N', 'YGeO2N', 'YSiO2N']
    Sb_pair = ['CaSbO2N', 'SrSbO2N']
    Perovskite = ['BaNbO2N','CaMoO2N','CaNbO2N','CeTaON2','GdTaON2','LaVO2N','SrMoO2N','SrNbO2N','SrTaO2N',
        'LaTiO2N', 'LaZrO2N','NdVO2N']
    fig = plt.figure(figsize=(3.5,4))
    ax = fig.add_axes([0.15,0.15,0.8,0.8])
    ax.scatter([data[x]['A/B'] for x in YSnO2N], [data[y]['B/X'] for y in YSnO2N], s=30,
        marker='p', label='YSnO$_{2}$N-type')
    ax.scatter([data[x]['A/B'] for x in LuMnO3], [data[y]['B/X'] for y in LuMnO3], s=30,
        marker='p', color='magenta', label='LuMnO$_{3}$-type')
    ax.scatter([data[x]['A/B'] for x in YSiO2N], [data[y]['B/X'] for y in YSiO2N], s=30,
        marker='s', color='red', label='YSiO$_{2}$N-type')
    ax.scatter([data[x]['A/B'] for x in Sb_pair], [data[y]['B/X'] for y in Sb_pair], s=30,
        marker='*', color='green', label='SrSbO$_{2}$N-type')
    ax.scatter([data[x]['A/B'] for x in Perovskite], [data[y]['B/X'] for y in Perovskite], s=30,
        marker='h', color='orange', label='Perovskite')
    ax.set_xlabel('r$_{A}$/r$_{B}$', fontsize=16, labelpad=0.1)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(0.5))
    ax.set_ylabel('r$_{B}$/r$_{X}$', fontsize=16)
    box = ax.get_position()
    ax.set_position([box.x0 + 0.05, box.y0,
        box.width - 0.01, box.height * 0.82])
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.32), fontsize=11, scatterpoints=1,
        ncol=2, handletextpad=0.1, borderpad=0.1, columnspacing=0.2)
#    plt.tight_layout()
    plt.savefig('C:/Users/steve/Pictures/Perovskite_tolerance.png', dpi=400)
    plt.show()