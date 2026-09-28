"""Project 4 - SDSS spectrum of NGC 1068 (M77): identify the lines, measure the redshift.

Reference solution, written to check that the task is doable in ~40 minutes.
Run:  python spectrum.py
"""
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from astroquery.sdss import SDSS
from scipy.optimize import curve_fit

PLATE, MJD, FIBER = 1070, 52591, 72            # NGC 1068 (M77), SDSS DR17
NAME = "NGC 1068"

# rest wavelengths in AIR (the values in most line lists)
LINES_AIR = {
    r"H$\beta$": 4861.33,
    "[O III]": 4958.91,
    "[O III] ": 5006.84,
    "[O I]": 6300.30,
    "[N II]": 6548.05,
    r"H$\alpha$": 6562.80,
    "[N II] ": 6583.45,
    "[S II]": 6716.44,
    "[S II] ": 6730.81,
}


def air_to_vac(lam):
    """Ciddor / IAU standard conversion, air -> vacuum (lambda in Angstrom)."""
    s2 = (1e4 / lam) ** 2
    n = 1 + 0.00008336624212083 + 0.02408926869968 / (130.1065924522 - s2) \
          + 0.0001599740894897 / (38.92568793293 - s2)
    return lam * n


def gauss_plus_line(x, amp, mu, sig, a, b):
    return amp * np.exp(-0.5 * ((x - mu) / sig) ** 2) + a * x + b


print("downloading the spectrum ...", flush=True)
hdul = SDSS.get_spectra(plate=PLATE, mjd=MJD, fiberID=FIBER)[0]
spec = hdul[1].data
lam = 10.0 ** spec["loglam"]        # vacuum, heliocentric frame (SDSS convention)
flux = spec["flux"]                 # 1e-17 erg/s/cm2/A
z_pipeline = hdul[2].data["Z"][0]
print(f"{len(lam)} pixels, {lam.min():.0f}-{lam.max():.0f} A, pipeline z = {z_pipeline:.5f}")

rows = []
for name, lam_air in LINES_AIR.items():
    lam_vac = air_to_vac(lam_air)
    guess = lam_vac * (1 + z_pipeline)
    m = np.abs(lam - guess) < 25
    if m.sum() < 10:
        continue
    p0 = [flux[m].max() - np.median(flux[m]), guess, 3.0, 0.0, np.median(flux[m])]
    try:
        p, cov = curve_fit(gauss_plus_line, lam[m], flux[m], p0=p0, maxfev=20000)
    except RuntimeError:
        continue
    if p[0] <= 0 or not 0.5 < p[2] < 25:
        continue
    lam_obs, err = p[1], np.sqrt(np.diag(cov))[1]
    rows.append((name, lam_air, lam_vac, lam_obs, err,
                 lam_obs / lam_vac - 1, lam_obs / lam_air - 1, 2.355 * p[2]))

print(f"\n{'line':10s} {'air':>9s} {'vac':>9s} {'observed':>10s} {'z(vac)':>9s} {'z(air)':>9s} {'FWHM':>7s}")
for n, la, lv, lo, e, zv, za, fw in rows:
    print(f"{n:10s} {la:9.2f} {lv:9.2f} {lo:10.2f} {zv:9.5f} {za:9.5f} {fw:7.1f}")

zv = np.array([r[5] for r in rows])
za = np.array([r[6] for r in rows])
c = 299792.458
print(f"\nz (vacuum rest wavelengths) = {zv.mean():.5f} +- {zv.std(ddof=1):.5f}"
      f"   ->  cz = {c*zv.mean():6.1f} km/s")
print(f"z (air rest wavelengths)    = {za.mean():.5f} +- {za.std(ddof=1):.5f}"
      f"   ->  cz = {c*za.mean():6.1f} km/s")
print(f"forgetting the air->vacuum correction costs {c*(zv.mean()-za.mean()):.1f} km/s")
print(f"SDSS pipeline z = {z_pipeline:.5f} (cz = {c*z_pipeline:.1f} km/s); "
      f"SDSS wavelengths are already heliocentric")

fig, ax = plt.subplots(2, 1, figsize=(11, 6.4), constrained_layout=True,
                       gridspec_kw={"height_ratios": [2, 1.4]})
ax[0].plot(lam, flux, lw=0.6, color="#2a78d6")
ax[0].set_xlim(3800, 9000)
ax[0].set_ylim(0, np.percentile(flux, 99.9) * 1.25)
for n, la, lv, lo, e, zvv, zaa, fw in rows:
    ax[0].axvline(lo, color="#eb6834", lw=0.6, alpha=0.6)
    ax[0].annotate(n.strip(), (lo, ax[0].get_ylim()[1] * 0.93), rotation=90,
                   ha="right", va="top", fontsize=8, color="#eb6834")
ax[0].set_ylabel(r"flux [10$^{-17}$ erg s$^{-1}$ cm$^{-2}$ $\AA^{-1}$]")
ax[0].set_title(f"{NAME}   SDSS {PLATE}-{MJD}-{FIBER}   z = {zv.mean():.5f}")

m = (lam > 6480) & (lam < 6800)
ax[1].plot(lam[m], flux[m], lw=0.9, color="#2a78d6")
for n, la, lv, lo, e, zvv, zaa, fw in rows:
    if 6480 < lo < 6800:
        ax[1].axvline(lo, color="#eb6834", lw=0.8)
        ax[1].annotate(n.strip(), (lo, flux[m].max() * 0.95), rotation=90,
                       ha="right", va="top", fontsize=8, color="#eb6834")
ax[1].set_xlabel(r"observed wavelength [$\AA$]")
ax[1].set_ylabel("flux")
ax[1].set_title(r"H$\alpha$ + [N II] + [S II]")
fig.savefig("spectrum.png", dpi=150)
print("\nwrote spectrum.png")
