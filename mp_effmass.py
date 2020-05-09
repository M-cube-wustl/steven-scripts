from sumo.electronic_structure.effective_mass import get_fitting_data, fit_effective_mass
import pymatgen
from pymatgen.ext.matproj import MPRester
from pymatgen.electronic_structure.core import Spin
import pprint

def mass_from_mp_ids(ids):
    """
    Arguments:
        ids: list of Materials Project ids
    Returns
        dict of {id:{elec:m_e, hole:m_h}}
    """
    masses = {}
    with MPRester("K2DZRTJAPkf4NpE3") as m:
        mp_entries = {id:m.get_bandstructure_by_material_id(id) for id in ids}
        for entry in mp_entries:
            masses[entry] = {
                'hole': call_sumo(mp_entries[entry], mp_entries[entry].get_vbm()),
                'elec': call_sumo(mp_entries[entry], mp_entries[entry].get_cbm())
            }
    pprint.pprint(masses)
    return masses

def call_sumo(bs, extreme):
    """
    Arguments:
        bs: Pymatgen BandStructureSymmLine object
        extreme: dict from BandStructure.get_cbm() or .get_vbm()
    Returns:
        (float) mass of lightest band of that type
    """
    masses = []
    for spin in [Spin.up, Spin.down]:
        for b_ind in extreme['band_index'][spin]:
            fit_data = get_fitting_data(bs, spin, 
                b_ind, extreme['kpoint_index'][0])[0]
            masses.append(fit_effective_mass(fit_data['distances'],
                fit_data['energies']))
            print(min([abs(mass) for mass in masses]))
    return min([abs(mass) for mass in masses])
