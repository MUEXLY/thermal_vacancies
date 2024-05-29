from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


def temp_beta_conversion(x: float) -> float:

    boltzmann_constant = 8.615e-5

    return 1 / (boltzmann_constant * x)


def main():

    beta_values, concentration = np.loadtxt(
        Path("outputs/concentration.txt")
    ).T

    fig, axs = plt.subplots(nrows=2, ncols=1, sharex=True)

    axs[0].plot(beta_values, concentration)
    axs[0].set_yscale("log")
    axs[0].set_ylabel(r"concentration $x_\text{V}$ (at. frac)")
    axs[0].grid()

    formation_energy = -np.diff(np.log(concentration)) / np.diff(beta_values)
    axs[1].plot(beta_values[1:], formation_energy)
    axs[1].set_ylabel(r"formation energy $E_\text{form}$ (eV)")
    axs[1].set_xlabel(r"inverse temperature $\beta$ (eV$^{-1}$)")
    axs[1].grid()

    secx = axs[0].secondary_xaxis(
        "top", functions=(temp_beta_conversion, temp_beta_conversion)
    )
    temperature_spacing = 100
    min_temperature = temperature_spacing * round(
        temp_beta_conversion(max(axs[0].get_xticks())) / temperature_spacing
    )
    max_temperature = temperature_spacing * round(
        temp_beta_conversion(min(axs[0].get_xticks())) / temperature_spacing
    )
    secx.set_xticks(
        np.arange(
            min_temperature,
            max_temperature + temperature_spacing,
            step=temperature_spacing,
        )
    )
    new_labels = [f"{x / 100:.0f}" for x in secx.get_xticks()]
    secx.set_xticklabels(new_labels)
    secx.set_xlabel("temperature ($10^2$ K)")

    fig.savefig(Path("concentration.pdf"))


if __name__ == "__main__":

    main()
