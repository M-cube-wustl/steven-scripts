import copy
import numpy as np
from pymatgen import Structure, MPRester
from pymatgen.transformations.standard_transformations import SubstitutionTransformation
from fireworks import LaunchPad, Firework, Workflow
from atomate.utils.utils import get_fws_and_tasks
from atomate.vasp.workflows.presets.core import wf_bandstructure
from atomate.vasp.fireworks.core import OptimizeFW, StaticFW
from atomate.vasp.powerups import add_bandgap_check, add_stability_check, add_modify_incar, add_tags

m = MPRester()

comp_list =  [
#    ['Mg','Sb',2],
#    ['Ca','Sb',2],
#    ['Sr','Sb',2],['Ba','Sb',2],
#    ['Mg','As',2],['Ca','As',2],['Sr','As',2],['Ba','As',2],
#    ['Mg','Bi',2],['Ca','Bi',2],['Sr','Bi',2],['Ba','Bi',2],

#    ['Sc','Sb',1],['La','Sb',1],['Y','Sb',1],['Eu','Sb',1],
#    ['Sc','Sb',1],['La','As',1],['Y','As',1],['Eu','As',1],
#    ['Sc','Sb',1],['La','Bi',1],['Y','Bi',1],['Eu','Bi',1],

#    ['Sc','Sn',2],['La','Sn',2],['Y','Sn',2],['Eu','Sn',2],#['Ce','Sn',1],
#    ['Sc','Sn',2],['La','Ge',2],['Y','Ge',2],['Eu','Ge',2],#['Ce','Ge',1],

#    ['Li','Te',2],['Na','Te',2],['K','Te',2],['Rb','Te',2],['Cs','Te',2],
#    ['Li','Se',2],['Na','Se',2],['K','Se',2],['Rb','Se',2],['Cs','Se',2],

#    ['Sc','Te',2],['La','Te',2],['Y','Te',2],['Eu','Te',2],#['Ce','Te',1],
#    ['Sc','Se',2],['La','Se',2],['Y','Se',2],['Eu','Se',2],#['Ce','Se',1],
   
#    ['Ce','As',2],['Ce','Sb',2],['Ce','Bi',2],
    
#    ['Ce','Ga',2],['Ce','In',2]
]


default_A='Sr'
default_B='Ta'
num_tilt_orders = 6
tilts_and_orders = []
site_num = 20
tilt_count = 15 #I have a bunch of old numbered poscars to ignore

other_dict = {
10: 'GePbO3',
11: 'GePbO3',
12: 'LiNbO3',
13: 'LiNbO3',
14: 'LiNbO3',
}

tetra_dict = {
15: 'AlSb',
16: 'BaGe',
17: 'BaSi',
18: 'CdSi',
19: 'GePb',
20: 'YSi'
}
    
for i in range(0,num_tilt_orders):
    filename = 'POSCAR-' + str(i + tilt_count) + '.vasp'
    tilts_and_orders.append(Structure.from_file(filename))
lpad = LaunchPad.auto_load()


#change cation composition
for composition in comp_list:
    tilt_count = 15 
    temp_structs = copy.deepcopy(tilts_and_orders)
    comp_tag = composition[0] + composition[1] + 'N' + 'O' + str(composition[2])
    struct_tag = 'tetra'
    for structure in temp_structs:
        if composition[2]==1:
            structure.replace_species({'O':'N','N':'O'})
        structure.replace_species({default_B:composition[1]}) #this will break if B-site is default_a but that shouldn't happen
        structure.replace_species({default_A:composition[0]})
        poscar_key = tetra_dict[tilt_count]

        opt = OptimizeFW(structure, vasp_cmd='ibrun tacc_affinity vasp_std')
        stat = StaticFW(parents=opt, vasp_cmd='ibrun tacc_affinity vasp_std')
        wf = Workflow([opt, stat])
        wf = add_modify_incar(wf, modify_incar_params={'incar_update':
            {'KPAR': 2, 'NCORE': 4, 'NSIM': 8, 'EDIFF': 0.000002, 'LMAXMIX': 6,
             'LSCALAPACK': '.FALSE.', 'ALGO': 'All'}})
        wf = add_modify_incar(wf, modify_incar_params={'incar_update':
            {'AMIX': 0.2, 'AMIX_MAG': 0.8, 'BMIX': 0.00001, 'BMIX_MAG': 0.00001,
             'ICHARG': 2, 'EDIFFG': 0.0005*site_num, 'KPAR': 1}},
              fw_name_constraint='structure optimization')
#           wf = add_stability_check(wf, fw_name_constraint = 'static') #default cutoff 0.1 eV/atom
        wf = add_tags(wf, (comp_tag, struct_tag, poscar_key))

        tilt_count = tilt_count + 1
        lpad.add_wf(wf)

