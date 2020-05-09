import csv
import pymatgen
import pprint
from pymatgen.ext.matproj import MPRester
from pymatgen.core.structure import Structure
from pymatgen.analysis.dimensionality import get_dimensionality_larsen
from pymatgen.analysis.local_env import get_neighbors_of_site_with_index, CrystalNN
from mp_effmass import call_sumo

def dict_status(dict, message):
    dict = {k:v for k,v in dict.items() if v != []}
    print(message, len([item for sublist in dict.values() for item in sublist]))
    return dict

def get_mass(formula_dict, rester):
    for key in formula_dict:
        for p in range(len(formula_dict[key])):
            try:
                if formula_dict[key][p]['bandstructure'] == None:
                    print('Fetching band structure from materials project')
                    formula_dict[key][p]['bandstructure'] = rester.get_bandstructure_by_material_id(
                        formula_dict[key][p]['material_id'])
                    print(formula_dict[key][p]['bandstructure'])
                formula_dict[key][p]['m_h'] = call_sumo(
                    formula_dict[key][p]['bandstructure'],
                    formula_dict[key][p]['bandstructure'].get_vbm())
                formula_dict[key][p]['m_e'] = call_sumo(
                    formula_dict[key][p]['bandstructure'],
                    formula_dict[key][p]['bandstructure'].get_cbm())
            except: #either we can't get a bandstructure or we can't get the mass
                formula_dict[key][p]['m_h'] = None
                formula_dict[key][p]['m_e'] = None

def get_dimension(formula_dict):
    for key in formula_dict:
        for p in range(len(formula_dict[key])):
            print(key)
            bonded_structure = CrystalNN().get_bonded_structure(
                formula_dict[key][p]['structure'])
            formula_dict[key][p]['dimensionality'] = get_dimensionality_larsen(
                bonded_structure)
            #formula_dict[key][p]['dimensionality'] = get_dimensionality_larsen(
            #    formula_dict[key][p]['structure'])
            print(formula_dict[key][p]['dimensionality'])
#cheon is slow for large structures, gorai is somewhat better, larsen is best

max_elements = 2
max_sites = 40
cent=["-1", "2/m", "mmm", "4/m", "4/mmm","-3", "-3m", "6/m", "6/mmm", "m-3", "m-3m"]
prop_list=["pretty_formula", "diel.poly_total", "band_gap","spacegroup.symbol",
    "spacegroup.point_group","e_above_hull", "material_id", "bandstructure","structure"]
excluded_elements = ['Tc','Ac','Th','Pa','U','Np','Pu']
with MPRester("K2DZRTJAPkf4NpE3") as m:
    structures = m.query(
        criteria=
        {
            "nelements":
                {"$lt":max_elements + 1
                },
            "nsites":
                {"$lt":max_sites + 1
                },
            "elements": 
                {"$nin":excluded_elements
                },
            "has": {"$in": ["bandstructure"]},
            "e_above_hull":
                {"$lt":0.1
                },
            "band_gap":
                {
                    "$gt":0.1,
                    "$lt":2
                },
        },
        properties=prop_list
     )
    structures = structures + (m.query(
        criteria=
        {
            "nelements":
                {"$lt":max_elements + 1
                },
            "nsites":
                {"$lt":max_sites + 1
                },
            "elements":
                {
                    "$all":['N'],
                    "$nin":excluded_elements
                },
            "has": {"$in": ["bandstructure"]},
            "e_above_hull":
                {
                    "$gt":0.1,
                    "$lt":0.2
                },
            "band_gap":
                {
                    "$gt":0.1,
                    "$lt":2
                }
        },
        properties=prop_list
    ))

    formula_dict = {}
    for structure in structures:
        if structure['pretty_formula'] not in formula_dict:
            formula_dict[structure['pretty_formula']] = [structure]
        else:
            formula_dict[structure['pretty_formula']].append(structure)
        
    formula_dict = dict_status(formula_dict, "Stable structures: ")
    for key in formula_dict:
        lowest = 0.1
        for polymorph in formula_dict[key]:
            if polymorph['e_above_hull'] < lowest:
                    lowest = polymorph['e_above_hull']
        formula_dict[key] = [p for p in formula_dict[key] if p['e_above_hull'] < (lowest + 0.05)]
    for key in formula_dict:    
        formula_dict[key] = [p for p in formula_dict[key] if  p['spacegroup.point_group'] not in cent]
    formula_dict = dict_status(formula_dict, "Metastable polar compounds: ")
    for key in formula_dict:
        formula_dict[key] = [p for p in formula_dict[key] if p['band_gap'] < 2.5 and p['band_gap'] > 0.10]
    formula_dict = dict_status(formula_dict, "Desired band gap: ")
    get_dimension(formula_dict)
    for key in formula_dict:
        formula_dict[key] = [p for p in formula_dict[key] if p['dimensionality']
            in ['3D', '3', 3, 'intercalated ion']]
    formula_dict = dict_status(formula_dict, "3D: ")
    get_mass(formula_dict, m)

            
#    empty_keys = []
#    for key in formula_dict:
#        if formula_dict[key] == []:
#            empty_keys.append(key)
#    for key in empty_keys:
#        del formula_dict[key]
#    empty_keys = []
#    for key in formula_dict:
#        if formula_dict[key][0]['diel.poly_total'] == None:
#            empty_keys.append(key)
#    for key in empty_keys:
#        del formula_dict[key]
#    empty_keys = []
#    for key in formula_dict:
#        if formula_dict[key][0]['diel.poly_total'] < 100:
#            empty_keys.append(key)
#    for key in empty_keys:
#        del formula_dict[key]
    
#    pprint.pprint(formula_dict)

    with open(str(max_elements) + 'polar.csv', 'w') as f:
        writer = csv.DictWriter(f, 
            fieldnames=formula_dict[next(iter(formula_dict.keys()))][0].keys() - ['bandstructure', 'structure'])
        writer.writeheader()
        for key in formula_dict.keys():
            for p in range(len(formula_dict[key])):
                row = {key:val for key, val in formula_dict[key][p].items() 
                    if key not in ['bandstructure', 'structure']}
                writer.writerow(row)

