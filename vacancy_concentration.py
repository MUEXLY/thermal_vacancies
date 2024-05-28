from pathlib import Path
from itertools import combinations


from numpy.typing import NDArray
import numpy as np


def get_chemical_potentials(occupying_energies_path: Path, reference_enthalpy_path: Path, data_file_path: Path) -> NDArray:

    occupying_energies = np.loadtxt(occupying_energies_path)
    enthalpy_per_atom = np.loadtxt(reference_enthalpy_path)

    num_sites, num_types = occupying_energies.shape
    atoms_header_line = None
    with open(data_file_path, "r") as file:
        for i, line in enumerate(file):
            if "Atoms # atomic" not in line:
                continue
            atoms_header_line = i
            break

    if not atoms_header_line:
        raise ValueError("header 'Atoms # atomic' not found before atom positions")
    
    types = np.loadtxt(data_file_path, skiprows=atoms_header_line + 2, max_rows=num_sites, usecols=1, dtype=int)
    concentrations = np.mean(types[:, None] == np.arange(1, num_types + 1), axis=0)

    type_pairs = list(combinations(range(num_types), r=2))

    coefficient_matrix = np.zeros((len(type_pairs) + 1, len(type_pairs) + 1))
    right_hand_vector = np.zeros(len(type_pairs) + 1)

    for i, (t1, t2) in enumerate(type_pairs):

        coefficient_matrix[i, t1] = 1.0
        coefficient_matrix[i, t2] = -1.0

        right_hand_vector[i] = np.mean(occupying_energies[:, t1] - occupying_energies[:, t2])

    coefficient_matrix[len(type_pairs), :] = concentrations
    right_hand_vector[len(type_pairs)] = enthalpy_per_atom

    chemical_potentials, *_ = np.linalg.lstsq(coefficient_matrix, right_hand_vector, rcond=None)
    return chemical_potentials


def main():

    occupying_energies_path = Path("outputs/occupying_energy.txt")
    reference_enthalpy_path = Path("outputs/enthalpy.txt")
    data_file_path = Path("outputs/relaxed.dat")

    chemical_potentials = get_chemical_potentials(occupying_energies_path, reference_enthalpy_path, data_file_path)

    vacant_energies_path = Path("outputs/vacant_energy.txt")
    vacant_energies = np.loadtxt(vacant_energies_path)
    occupying_energies = np.loadtxt(occupying_energies_path)
    num_sites, num_types = occupying_energies.shape
    
    formation_energies = np.repeat(vacant_energies[..., None], repeats=num_types, axis=1) - occupying_energies + np.repeat(chemical_potentials[None, ...], repeats=num_sites, axis=0)
    beta_values = np.linspace(10.0, 30.0, 10_000)
    local_probabilities = 1.0 / (
        1.0 + np.sum(
            np.exp(beta_values[:, np.newaxis, np.newaxis] * formation_energies[np.newaxis, :, :]),
            axis=2
        )
    )
    concentration = np.mean(local_probabilities, axis=1)
    
    output_path = Path("outputs/concentration.txt")
    with open(output_path, "w") as file:
        np.savetxt(
            file,
            np.vstack((beta_values, concentration)).T,
            header="beta x_V"
        )


if __name__ == "__main__":

    main()
