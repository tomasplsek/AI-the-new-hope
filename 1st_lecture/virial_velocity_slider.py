import os
import numpy as np
import matplotlib

# If running without a display, use a non-interactive backend and save a PNG.
HEADLESS = os.environ.get("DISPLAY", "") == "" and os.name != "nt"
if HEADLESS:
    matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Gravitational constant in astrophysical units:
# G = 4.302e-6 kpc (km/s)^2 / Msun
G = 4.302e-6

# Radius array
R_mpc = np.linspace(0.1, 3.0, 500)   # Mpc
R_kpc = R_mpc * 1000.0               # kpc

# Initial cluster mass
M0 = 5e14  # solar masses


def virial_velocity(M, R_kpc):
    """
    Compute characteristic virial velocity in km/s.

    Parameters
    ----------
    M : float
        Mass in solar masses.
    R_kpc : array-like
        Radius in kpc.

    Returns
    -------
    array-like
        Virial velocity in km/s.
    """
    return np.sqrt(G * M / R_kpc)


# Initial velocity profile
v0 = virial_velocity(M0, R_kpc)

# Create figure
fig, ax = plt.subplots(figsize=(8, 6))
plt.subplots_adjust(bottom=0.25)

# Plot initial profile
(line,) = ax.plot(R_mpc, v0, lw=2, color="tab:blue")

ax.set_xlabel("Radius R [Mpc]")
ax.set_ylabel("Virial Velocity [km/s]")
ax.set_title(rf"Galaxy Cluster Virial Velocity Profile, $M = {M0:.2e}\ M_\odot$")
ax.grid(True, alpha=0.35)
ax.set_ylim(0, 5000)

# Slider axis
ax_mass = plt.axes([0.2, 0.1, 0.6, 0.03])

# Slider for log10 mass
mass_slider = Slider(
    ax=ax_mass,
    label=r"$\log_{10}(M/M_\odot)$",
    valmin=13.0,
    valmax=16.0,
    valinit=np.log10(M0),
    valstep=0.01,
)


def update(val):
    logM = mass_slider.val
    M = 10.0**logM
    v = virial_velocity(M, R_kpc)
    line.set_ydata(v)
    ax.set_title(rf"Galaxy Cluster Virial Velocity Profile, $M = {M:.2e}\ M_\odot$")
    fig.canvas.draw_idle()


mass_slider.on_changed(update)

output = "virial_velocity_profile.png"
fig.savefig(output, dpi=150, bbox_inches="tight")
print(f"Saved initial plot to {output}")

if HEADLESS:
    print("No display detected, so the interactive slider window was not opened.")
else:
    plt.show()
