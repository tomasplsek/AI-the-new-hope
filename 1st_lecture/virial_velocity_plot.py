import numpy as np

# Request an interactive GUI backend so the slider window stays open.
# TkAgg is commonly available with standard Python installs.
import matplotlib
try:
    matplotlib.use("TkAgg")
except Exception:
    # If TkAgg is unavailable, Matplotlib will fall back to its default backend.
    pass

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Constants
G = 4.30091e-6  # Gravitational constant in kpc (km/s)^2 / Msun

# Radius range: 0.1 to 3 Mpc
R_mpc = np.linspace(0.1, 3.0, 300)
R_kpc = R_mpc * 1000  # convert Mpc to kpc

# Initial cluster mass
M0 = 5e14  # solar masses


def virial_velocity(M, R_kpc):
    """Return virial velocity in km/s for mass M [Msun] and radius R [kpc]."""
    return np.sqrt(G * M / R_kpc)


# Initial velocity curve
v0 = virial_velocity(M0, R_kpc)

# Create figure and leave room at the bottom for the slider
fig, ax = plt.subplots(figsize=(8, 5.5))
plt.subplots_adjust(bottom=0.25)

# Plot initial curve
(line,) = ax.plot(R_mpc, v0, linewidth=2)

ax.set_xlabel("Radius [Mpc]")
ax.set_ylabel("Virial Velocity [km/s]")
ax.set_title(rf"Virial Velocity vs. Radius, $M = {M0:.2e}\,M_\odot$")
ax.grid(True)

# Set sensible y-limits based on max mass in slider range
M_min = 1e14
M_max = 1e15
v_max = virial_velocity(M_max, R_kpc).max()
ax.set_ylim(0, 1.1 * v_max)

# Slider axis: [left, bottom, width, height]
slider_ax = fig.add_axes([0.18, 0.08, 0.68, 0.04])

mass_slider = Slider(
    ax=slider_ax,
    label=r"Mass [$10^{14}\,M_\odot$]",
    valmin=M_min / 1e14,
    valmax=M_max / 1e14,
    valinit=M0 / 1e14,
    valstep=0.1,
)


def update(val):
    """Update plot when the mass slider changes."""
    M = mass_slider.val * 1e14
    v = virial_velocity(M, R_kpc)
    line.set_ydata(v)
    ax.set_title(rf"Virial Velocity vs. Radius, $M = {M:.2e}\,M_\odot$")
    fig.canvas.draw_idle()


mass_slider.on_changed(update)

plt.show(block=True)
