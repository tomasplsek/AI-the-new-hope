#!/usr/bin/env python3
"""Estimate the virial velocity and ICM virial temperature of a galaxy cluster."""

import math

# Inputs
mass_solar_masses = 5e14   # cluster mass in solar masses
radius_mpc = 1.0           # cluster radius in Mpc
mu = 0.59                  # mean molecular weight for fully ionized primordial gas

# Constants
G = 4.30091e-6             # kpc (km/s)^2 / solar mass
m_p = 1.67262192369e-27    # proton mass in kg
k_B = 1.380649e-23         # Boltzmann constant in J/K
keV_per_joule = 1.0 / 1.602176634e-16

# Convert radius from Mpc to kpc
radius_kpc = radius_mpc * 1000.0

# Virial/circular velocity estimate: v = sqrt(GM/R)
virial_velocity_kms = math.sqrt(G * mass_solar_masses / radius_kpc)

# Virial temperature estimate for the intracluster medium:
# k_B T ~ (1/2) mu m_p v^2
virial_velocity_ms = virial_velocity_kms * 1000.0
virial_temperature_K = mu * m_p * virial_velocity_ms**2 / (2.0 * k_B)
virial_temperature_keV = k_B * virial_temperature_K * keV_per_joule

print(f"Mass: {mass_solar_masses:.2e} solar masses")
print(f"Radius: {radius_mpc:.2f} Mpc")
print(f"Virial velocity: {virial_velocity_kms:.1f} km/s")
print(f"ICM virial temperature: {virial_temperature_K:.2e} K")
print(f"ICM virial temperature: {virial_temperature_keV:.2f} keV")
