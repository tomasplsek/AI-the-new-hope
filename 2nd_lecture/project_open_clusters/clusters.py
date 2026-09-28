"""Open clusters with Gaia DR3: members by clustering, HR diagrams, rough ages.

Reference solution written to check that the project is doable in ~40 minutes
of prompting an agent.  Run:  python clusters.py

Note: the full gaiadr3.gaia_source table times out at the moment (DR4 prep),
gaiadr3.gaia_source_lite + cone_search_async is fast and has everything we need.
"""
import warnings
warnings.filterwarnings("ignore")

import matplotlib
matplotlib.use("Agg")

import os

import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np
from astropy.coordinates import SkyCoord
from astroquery.gaia import Gaia
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

Gaia.MAIN_GAIA_TABLE = "gaiadr3.gaia_source_lite"
Gaia.ROW_LIMIT = -1

#                    RA        Dec      cone    literature age
CLUSTERS = {
    "Pleiades (M45)": (56.750, 24.1167, 1.2, "125 Myr"),
    "Praesepe (M44)": (130.100, 19.6667, 1.0, "700 Myr"),
    "M67":            (132.825, 11.8000, 0.6, "4 Gyr"),
}
GMAX = 18.0


def fetch(name, ra, dec, radius):
    """Cone search, cached on disk so re-runs are instant."""
    cache = name.split()[0].lower().strip("()") + ".ecsv"
    if os.path.exists(cache):
        from astropy.table import Table
        t = Table.read(cache)
    else:
        t = Gaia.cone_search_async(SkyCoord(ra, dec, unit="deg"),
                                   radius=radius * u.deg).get_results()
        t = t["source_id", "ra", "dec", "parallax", "parallax_over_error",
              "pmra", "pmdec", "phot_g_mean_mag", "bp_rp", "ruwe"]
        t.write(cache, overwrite=True)
    keep = (np.isfinite(t["pmra"]) & np.isfinite(t["pmdec"]) & np.isfinite(t["bp_rp"])
            & (t["phot_g_mean_mag"] < GMAX)
            & (t["parallax_over_error"] > 10))          # good distances only
    return t[keep]


def members(t):
    """DBSCAN in (pmra, pmdec, parallax).

    The trap: the BIGGEST clump is the Galactic field behind the cluster, and
    DBSCAN finds it first.  The cluster we want is the NEAREST clump - the one
    with the largest parallax - so pick by that, not by size.
    """
    X = np.column_stack([t["pmra"], t["pmdec"], t["parallax"]]).astype(float)
    Xs = StandardScaler().fit_transform(X)
    lab = DBSCAN(eps=0.08, min_samples=30).fit_predict(Xs)
    best, best_plx = None, -np.inf
    for k in set(lab) - {-1}:
        g = lab == k
        if g.sum() < 50:
            continue
        if np.median(X[g, 2]) > best_plx:
            best, best_plx = k, np.median(X[g, 2])
    return np.zeros(len(t), bool) if best is None else lab == best


fig, axes = plt.subplots(2, len(CLUSTERS), figsize=(13, 7.6), constrained_layout=True)
summary = []

for i, (name, (ra, dec, rad, age_lit)) in enumerate(CLUSTERS.items()):
    print(f"\n=== {name} ===", flush=True)
    t = fetch(name, ra, dec, rad)
    m = members(t)
    plx = np.array(t["parallax"][m], float)
    dist = 1000.0 / np.median(plx)
    dm = 5 * np.log10(dist) - 5                       # distance modulus
    MG = np.array(t["phot_g_mean_mag"][m], float) - dm
    col = np.array(t["bp_rp"][m], float)

    # crude turn-off: the bluest few percent of the members
    bright = MG < 5
    turn = np.percentile(col[bright], 3) if bright.sum() > 20 else np.percentile(col, 3)
    summary.append((name, m.sum(), np.median(plx), dist, turn, age_lit))
    print(f"{len(t)} sources, {m.sum()} members, plx = {np.median(plx):.3f} mas, "
          f"d = {dist:.0f} pc, turn-off BP-RP = {turn:.2f}, literature {age_lit}")

    a = axes[0, i]
    a.scatter(t["pmra"][~m], t["pmdec"][~m], s=1, c="0.85", lw=0)
    a.scatter(t["pmra"][m], t["pmdec"][m], s=4, c="#2a78d6", lw=0)
    a.set_xlim(np.median(t["pmra"][m]) - 30, np.median(t["pmra"][m]) + 30)
    a.set_ylim(np.median(t["pmdec"][m]) - 30, np.median(t["pmdec"][m]) + 30)
    a.set_xlabel(r"$\mu_{\alpha*}$ [mas/yr]")
    a.set_ylabel(r"$\mu_\delta$ [mas/yr]")
    a.set_title(f"{name}\n{m.sum()} members, d = {dist:.0f} pc")

    b = axes[1, i]
    b.scatter(col, MG, s=5, c="#2a78d6", lw=0)
    b.axvline(turn, color="#eb6834", lw=1.2, ls="--")
    b.invert_yaxis()
    b.set_xlim(-0.5, 3.5)
    b.set_ylim(12, -3)
    b.set_xlabel(r"$BP-RP$")
    b.set_ylabel(r"$M_G$")
    b.set_title(f"turn-off $BP-RP$ = {turn:.2f}   (lit. {age_lit})")

fig.savefig("clusters.png", dpi=150)
print("\nwrote clusters.png\n")
print(f"{'cluster':16s} {'N':>5s} {'plx':>7s} {'d [pc]':>8s} {'turn-off':>9s} {'lit. age':>9s}")
for n, N, p, d, turn, age in summary:
    print(f"{n:16s} {N:5d} {p:7.3f} {d:8.0f} {turn:9.2f} {age:>9s}")
print("\nbluer turn-off = younger cluster")
