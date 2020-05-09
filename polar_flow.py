import numpy as np
from pymatgen import Structure
from fireworks import LaunchPad, Workflow
from atomate.vasp.powerups import add_modify_incar, add_tags
from atomate.vasp.workflows.base.ferroelectric import get_wf_ferroelectric


comp = 'LaSnO2N'
np_struct = Structure.from_file(comp + '_hex_30.vasp')
p_struct = Structure.from_file(comp + '_dist.vasp')
wf = get_wf_ferroelectric(p_struct, np_struct, vasp_cmd='ibrun tacc_affinity vasp_std',
    add_analysis_task=True, tags=[comp], db_file='/scratch/04391/tg836903/ilmenites/db.json')
wf = add_modify_incar(wf, modify_incar_params={'incar_update':
    {'Algo': 'Normal', 'EDIFF': 0.00001, 'NEDOS':3000}})
    
lpad = LaunchPad.auto_load() # loads this based on the FireWorks configuration
lpad.add_wf(wf)

