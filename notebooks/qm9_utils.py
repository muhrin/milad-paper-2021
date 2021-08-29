import collections
import json
import random

import pymatgen.io.ase
from pymatgen import symmetry
import numpy as np

import milad
from milad import asetools
from milad import atomic
from milad import optimisers

# The atomic numbers of the allowed species
species = (1, 6, 7, 8, 9)
SPECIES_MAP = dict(numbers=tuple(species), range=(1., 2.))
FEATURES = dict(type=milad.functions.WeightedDelta, map_species_to='WEIGHT')
CUTOFF = 5.
CUTOFF_FACTOR = 1.25


def create_moments_calculator(cutoff: float, max_order:int = 7):
    calculator = milad.functions.Chain(
        # Scale to fit within cutoff sphere
        atomic.ScalePositions(1. / cutoff),
        # Map the atoms onto a feature function
        atomic.FeatureMapper(**FEATURES),
        # Calculate Zernike moments up to the maximum order
        milad.zernike.ZernikeMomentsCalculator(max_order)
    )
    
    return calculator


def create_descriptor(invariants, cutoff: float, apply_cutoff=True, max_order=None):
    max_order = max_order or invariants.max_order
    return milad.descriptor(
        species={'map': SPECIES_MAP},
        features=FEATURES,
        cutoff=cutoff,
        invs=invariants,
        moments_calculator=milad.ZernikeMomentsCalculator(max_order),
        apply_cutoff=apply_cutoff,
    )


def get_lowest_rmsd_results(frame):
    results = {}
    for idx in frame['QM9 ID'].unique():
        filtered = frame[frame['QM9 ID'] == idx].sort_values('RMSD')
        results[idx] = filtered['Result'].iloc[0]

    return results


def load_test_set() -> dict:
    """Get the subset of QM9 ids we will be using"""
    with open('qm9_subset.json', 'r') as subset:
        test_set = json.load(subset)
    
    return {int(key): value for key, value in test_set.items()}


def get_best_reconstruction(idx, dataset):
    # Get the row with the minimum RMSD for that index
    attempts = dataset.loc[dataset['QM9 ID'] == idx]
    min_rmsd = attempts['RMSD'].min()
    return attempts.loc[attempts['RMSD'] == min_rmsd]


def create_initial_atoms(num_atoms: int, max_radius: float, minsep=0.85, include_species=False):
    initial = atomic.random_atom_collection_in_sphere(num_atoms, max_radius, centre=True, numbers=1.)
    
    optimiser = optimisers.LeastSquaresOptimiser()
    separation_force = atomic.SeparationForce(epsilon=1e-8, cutoff=minsep, power=12)
    mask = initial.get_mask()
    mask.numbers[:] = 1.
    res = optimiser.optimise(
        separation_force,
        initial,
        mask=mask
    )

    initial = res.value
    
    if include_species:
        # Set the species appropriately
        initial.numbers = np.array(random.choices(species, k=num_atoms))
        
    return initial


def get_point_groups(
    qm9data, 
    test_set,
    ignore_species=False
):
    results = collections.defaultdict(dict)
    adapter = pymatgen.io.ase.AseAtomsAdaptor()
    
    for size, ids in test_set.items():
        for qm9id in ids:
            molecule = qm9data.get_atoms(idx=qm9id)
            if ignore_species:
                molecule.numbers[:] = 1.
            asetools.prepare_molecule(molecule)

            mol = adapter.get_molecule(molecule)
            
            mol.get_centered_molecule = lambda: mol
            
            analyser = symmetry.analyzer.PointGroupAnalyzer(mol)
            pg = analyser.get_pointgroup()

            results[size][qm9id] = pg
    
    return results


def order_by_pointgroup(results: dict):
    # Expecting results to be a dict of [size, dict] where the second dict
    # contains [id, pointgroup] pairs
    ordered = collections.defaultdict(list)
    for size, entry in results.items():
        for qm9id, pg in entry.items():
            ordered[str(pg)].append(qm9id)
    return ordered
