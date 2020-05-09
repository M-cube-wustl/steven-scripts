import numpy as np
import gzip
import itertools
import os
import re
import pprint
import copy
from pymatgen import Structure, MPRester
from pymatgen.analysis.phase_diagram import PhaseDiagram
from pymatgen.io.vasp import Vasprun
from pymatgen.io.vasp.sets import get_vasprun_outcar
from pymatgen.core.structure import Structure
from pymatgen.core.composition import Composition
from pymatgen.entries.computed_entries import ComputedEntry
from pymatgen.entries.compatibility import MaterialsProjectCompatibility
from atomate.vasp.database import VaspCalcDb
import pandas as pd

PATH_TO_MY_DB_JSON = '/work/04391/tg836903/stampede2/atomate/config/db.json'
atomate_db = VaspCalcDb.from_db_file(PATH_TO_MY_DB_JSON)  #database of ALL calcs
output_dict = {}

comp_list = [
# 'LaPbNO2','SbPbNO2', 'AsPbNO2', 'TlSnNO2', 'BaBiNO2', #'LaSeNO2'
# ,'CeGeN2O', 'ZrSiN2O', 'LaSbN2O', 'TaGaNO2', 'CeAsNO2', 'CeGaNO2',
#    'CeGeNO2', 'BiAsN2O', 'CeSnN2O', 'TiGeNO2', 'LaSnNO2', 'LaBiN2O', 'BaBiNO2', 'SrBiNO2',
#    'CeBiN2O', 'SrSbNO2', 'CaSbNO2', 'CaBiNO2', 'CeSiN2O', 'ZrGeN2O', 'ZrAsNO2', 'LaGeNO2',
#    'CeSbNO2', 'CeInNO2', 'GeBiNO2', 'NdSnNO2', 'ScGeNO2', 'LaAsN2O', 'CeSbN2O', 'YSbN2O',
#    'YSnNO2', 'BaTeN2O', 'SrTeN2O', 'LuSnNO2', 'CaTeN2O', 'HfSiN2O', 'NbSiN2O', 'TiSiN2O',
#    'VSiN2O', 'HfGeN2O', 'SiWN2O', 'SiMoN2O', 'ReSiN2O', 'NbGeN2O', 'CeSnNO2', 'NdGeNO2',
#    'GaBiN2O', 'ZrGaNO2', 'HfAsNO2', 'LuGeNO2', 'NdBiN2O', 'SnBiNO2', 'LuSbN2O', 'NbAsN2O',
#    'NbAsNO2', 'NdSbN2O', 'YGeNO2', 'CeAsN2O', 'YAsN2O', 'LuAsN2O', 'LuSiNO2', 'SiBiNO2',
#    'NdSiNO2', 'VGeN2O', 'CeSiNO2', 'LaSiNO2', 'NbSiNO2', 'BaSbNO2', 'SiMoNO2', 'CaAsNO2',
#    'SrAsNO2', 'MgAsNO2', 'YBiN2O', 'MgTeN2O', 'MgSbNO2', 'NdZrNO2', 'CaNbNO2', 'LaZrNO2',
#    'LaVNO2', 'NdVNO2', 'SrNbNO2', 'BaNbNO2', 'LaNbN2O', 'CaMoNO2', 'SrMoNO2', 'CeTaN2O',
#    'CeTiNO2', 'AsPbN2O', 'NdPbN2O', 'TlGeN2O', 'TlTeN2O', 'TlAsNO2', 'GePbNO2', 'TlGeNO2',
#    'TlSiNO2', 'LaPbNO2', 'TlSbN2O', 'SbPbNO2', 'AsPbNO2', 'TlTeNO2', 'GePbN2O', 'CePbN2O',
#    'TlAsN2O', 'TlSnNO2', 'SbMoN2O', 'SnPbN2O', 'GaPbNO2', 'LuPbNO2', 'CePbNO2', 'CeTlNO2',
#    'YPbNO2', 'BiPbNO2', 'NdPbNO2', 'SiPbN2O', 'NdAsN2O', 'InPbNO2', 'VAsNO2', 'ScBiN2O',
#    'NdTeNO2', 'YSiNO2', 'NbSbNO2', 'ZrSbNO2', 'TaSiNO2', 'NbGeNO2', 'GeMoNO2', 'TiSbNO2',
#    'LuTeNO2', 'GaReNO2', 'MgBiNO2', 'MoAsN2O', 'ScPbNO2', 'ScSnNO2', 'TaGeN2O', 'TiSnN2O',
#    'VTeN2O', 'TaAsNO2', 'ZrInNO2', 'GaWNO2', 'NbGaN2O', 'TlBiN2O', 'HfInNO2', 'LuBiN2O',
#    'BiTeNO2', 'HfPbN2O', 'ScSbN2O', 'VSbNO2', 'NbPbN2O', 'CeTeN2O', 'VGaNO2', 'HfSbNO2',
#    'NbGaNO2', 'ZrPbN2O', 'TiSbN2O', 'AsWNO2', 'TlPbNO2', 'TiAsN2O', 'AsWN2O', 'ZrSnN2O',
#    'GeMoN2O', 'TaAsN2O', 'ScSiNO2', 'VSiNO2', 'YTeNO2', 'TaSiN2O', 'TiSiNO2', 'NbSnN2O',
#    'BaAsNO2', 'HfSnN2O', 'TiAsNO2', 'TaGaN2O', 'VSnN2O', 'TiBiNO2', 'GaMoNO2', 'VBiNO2',
#    'TiGaNO2', 'ReAsNO2', 'CeBiNO2', 'ZrTlNO2', 'TaGeNO2', 'TiTeN2O', 'ReGeN2O', 'HfGaNO2',
#    'MoAsNO2', 'ScAsN2O', 'LaTeNO2', 'KSeNO2', 'NaSeNO2', 'RbTeNO2', 'NaTeNO2', 'CsTeNO2',
#    'EuAsN2O', 'EuGeNO2', 'RbSeNO2', 'KTeNO2', 'CeSeN2O', 'EuSbN2O', 'CsSeNO2', 'LiSeNO2',
#    'LiTeNO2', 'ScTeNO2', 'EuSnNO2', 'ScSeNO2', 'YSeNO2', 'EuBiN2O', 'EuSeNO2', 'EuTeNO2',
    'InSnNO2', 'GaSnNO2', 'SnSbNO2', 'NbSnNO2', 'TaSnNO2'#,
#    'GaGeNO2', 'ZnSbNO2', 'YSbNO2'
]



#test_list = ['SnBiNO2','LaSnPS2']
#chemsys_list = [['Sn','Bi','N','O'],['La','Sn','P','S']]

#tiny_list = [ ['Zn','Sb',2],['Y','Sb',2]
#['Sc','Sn',2],['Y','Sn',2],['Nd','Sn',2],['Ca','Sb',2],['Ba','Sb',2],['Sn','Bi',2],
#    ['Sr','Sb',2],['Ca','As',2],['Ba','As',2],['La','Ge',2],['Sr','As',2],['Ga','Ge',2],
#    ['Y','Ge',2],['Sc','Sn',2],['La','Sn',2],['Eu','Sn',2],['Ga','Sn',2],['In','Sn',2],
#    ['Sn','Sb',2],['Ba','Bi',2],['Sr','Bi',2],['Nb','Sn',2],['Ta','Sn',2]
#    ]

def biased_hull(atomate_db, comp_list, anions=['N','O'], bias=[0]):
    with MPRester() as mpr:
        for pretty in comp_list:
            composition = Composition(pretty)
            composition = [str(i) for i in composition.elements]
 #           anion_num = composition[2]
 #           composition.pop()
 #           composition.append(anions[0])
 #           composition.append(anions[1])
        #First, build the phase diagram and hull
            orig_entries = mpr.get_entries_in_chemsys(composition)
            #orig_entries = mpr.get_entries_in_chemsys(chemsys_list[k])
            entries = []
            for i in range(len(bias)):
                entries.append(copy.deepcopy(orig_entries))
                for j in range(0,len(entries[i])):
                    temp = entries[i][j].parameters['potcar_symbols']
                    if temp in [['PBE ' + anions[0]], ['PBE ' + anions[1]], 
                    ['PBE ' + anions[0], 'PBE '+ anions[1]], ['PBE ' + anions[1], 'PBE ' + anions[0]]]:
                        new_entry = ComputedEntry(entries[i][j].composition, 
                            entries[i][j].energy + bias[i]) #add arbitrary energy to gas phase
                        entries[i][j] = copy.deepcopy(new_entry)

    #Then, find each entry in atomate_db which has this composition and get its hull energy
            print(pretty)
            structures = []
            cursor = atomate_db.collection.find({'task_label': 'static', 
                'formula_pretty': pretty})
            for structure in cursor:
                structures.append(structure)
            struct_entries = []
            for structure in structures:
                temp = structure['calcs_reversed'][0]
                struct_entry = ComputedEntry(temp['composition_unit_cell'],temp['output']['energy'],
                    parameters = {'run_type': temp['run_type'],
                        'is_hubbard': structure['input']['is_hubbard'],
                        'pseudo_potential': structure['input']['pseudo_potential'],
                        'hubbards': structure['input']['hubbards'],
                        'potcar_symbols': structure['orig_inputs']['potcar']['symbols'],
                        'oxide_type': 'oxide'}, data = {'oxide_type': 'oxide'})
                for i in range(0,4):
                    struct_entry.parameters['potcar_symbols'][i] = 'PBE ' + struct_entry.parameters['potcar_symbols'][i]
                struct_entry = MaterialsProjectCompatibility().process_entries(
                    [struct_entry])[0] #takes list as argument and returns list
                struct_entries.append(struct_entry)
            bias_strings = []
            stable_polymorph = {'id': 0, 'tilt_order': ''}
            for i in range(len(bias)):
                entries[i].extend(struct_entries)
                pd = PhaseDiagram(entries[i])
                bias_string = 'ehull_' + str(bias[i]) + 'eV'
                bias_strings.append(bias_string)
                stable_polymorph[bias_strings[i]] = 1000
                print(bias_strings)
                for j in range(0,len(struct_entries)):
                    stability = pd.get_decomp_and_e_above_hull(struct_entries[j])
                    print(structures[j]['formula_pretty'],structures[j]['task_id'],
                        [phase.composition for phase in stability[0]],stability[1])
                    if stability[1] < stable_polymorph[bias_strings[i]]:
                        stable_polymorph['id'] = structures[j]['task_id']
                        stable_polymorph[bias_strings[i]] = stability[1]
                    if 'tags' in structures[j]:
                        if structures[j]['tags'][1] == 'tetra':
                            stable_polymorph['tilt_order'] = structures[j]['tags'][2]
                        else:
                            stable_polymorph['tilt_order'] = structures[j]['tags'][1]
                    output_dict[structures[j]['formula_pretty']] = stable_polymorph
        return output_dict

final_dict = biased_hull(atomate_db, comp_list, bias = [0,16])
final_dict['SrTaNO2'] = {
    'ehull_0eV': 0
}
final_dict['CaTaNO2'] = {
    'ehull_0eV': 0.01
}
final_dict['BaTaNO2'] = {
    'ehull_0eV': 0.012
}

final_dict['LaTiNO2'] = {
    'ehull_0eV': 0.038
}
pprint.pprint(final_dict)
out_frame = pd.DataFrame.from_dict(final_dict)
out_frame = out_frame.transpose()
out_frame.to_csv('Oxynitride_hull_energies.csv')


#tiny_dict = biased_hull(atomate_db, tiny_list)
#pprint.pprint(tiny_dict)
#dict_1 = biased_hull(atomate_db, [['La','Sn', 2]], anions=['P','O'])
#pprint.pprint(dict_1)
#dict_2 = biased_hull(atomate_db, [['La','Sn', 2]], anions=['P','S'])
#pprint.pprint(dict_2)
#dict_3 = biased_hull(atomate_db, [['La','Sn', 1]], anions=['S','N'])
#pprint.pprint(dict_2)

