import json

import milad
from milad import atomic

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
        milad.zernike.ZernikeMomentCalculator(max_order)
    )
    
    return calculator


def create_descriptor(invariants, cutoff: float, apply_cutoff=True, max_order=None):
    max_order = max_order or invariants.max_order
    return milad.descriptor(
        species={'map': SPECIES_MAP},
        features=FEATURES,
        cutoff=cutoff,
        invs=invariants,
        moments_calculator=milad.ZernikeMomentCalculator(max_order),
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