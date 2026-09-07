import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

SOLAR_RADIUS_IN_EARTH_RADII = 109.076


def mass_radius_relation(
    polytropic_index: float, mu_e: float
) -> tuple[np.ndarray, np.ndarray, float]:
    masses_solar = np.linspace(0.2, 1.38, 500)
    chandrasekhar_mass = 5.83 / (mu_e**2)

    radius_scale = 0.0127 * SOLAR_RADIUS_IN_EARTH_RADII * (2.0 / mu_e) ** (5.0 / 3.0)
    low_mass_power = (1.0 - polytropic_index) / (3.0 - polytropic_index)
    cutoff = np.clip(1.0 - (masses_solar / chandrasekhar_mass) ** (4.0 / 3.0), 0.0, None)

    radii_earth = radius_scale * masses_solar**low_mass_power * np.sqrt(cutoff)
    valid = masses_solar < chandrasekhar_mass
    return masses_solar[valid], radii_earth[valid], chandrasekhar_mass


def main() -> None:
    initial_index = 1.5
    initial_mu_e = 2.0

    masses_solar, radii_earth, chandrasekhar_mass = mass_radius_relation(
        initial_index, initial_mu_e
    )

    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.28, top=0.78)

    (line,) = ax.plot(masses_solar, radii_earth, label="WD mass-radius curve")
    ax.set_title("White Dwarf Radius vs Mass")
    ax.set_xlabel("Mass (M_sun)")
    ax.set_ylabel("Radius (R_earth)")
    ax.grid(True)
    ax.legend()
    ax.set_xlim(masses_solar[0], masses_solar[-1])
    ax.set_ylim(0.0, radii_earth.max() * 1.1)

    info_text = ax.text(
        0.02,
        0.95,
        f"Chandrasekhar mass: {chandrasekhar_mass:.2f} M_sun",
        transform=ax.transAxes,
        va="top",
    )
    fig.text(
        0.12,
        0.95,
        "R = R0 * M^((1-n)/(3-n)) * sqrt(1 - (M / M_ch)^(4/3))\n"
        "M_ch = 5.83 / mu_e^2",
        va="top",
    )

    ax_index = plt.axes([0.15, 0.12, 0.7, 0.03])
    ax_mu_e = plt.axes([0.15, 0.06, 0.7, 0.03])

    slider_index = Slider(
        ax=ax_index,
        label="n",
        valmin=1.1,
        valmax=2.5,
        valinit=initial_index,
    )
    slider_mu_e = Slider(
        ax=ax_mu_e,
        label="mu_e",
        valmin=1.5,
        valmax=2.5,
        valinit=initial_mu_e,
    )

    def update(_: float) -> None:
        mass_values, radius_values, ch_mass = mass_radius_relation(
            slider_index.val, slider_mu_e.val
        )
        line.set_xdata(mass_values)
        line.set_ydata(radius_values)
        ax.set_xlim(mass_values[0], mass_values[-1])
        ax.set_ylim(0.0, radius_values.max() * 1.1)
        info_text.set_text(f"Chandrasekhar mass: {ch_mass:.2f} M_sun")
        fig.canvas.draw_idle()

    slider_index.on_changed(update)
    slider_mu_e.on_changed(update)

    if len(sys.argv) > 1:
        fig.savefig(sys.argv[1])
    else:
        plt.show()


if __name__ == "__main__":
    main()
