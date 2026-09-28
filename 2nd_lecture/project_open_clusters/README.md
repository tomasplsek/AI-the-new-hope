# Project: open clusters with Gaia DR3

Reference solution (`clusters.py`) — written and run to check that the project is
really doable in ~40 minutes of prompting an agent.

## What it does

1. Gaia DR3 cone search for **Pleiades (M45)**, **Praesepe (M44)** and **M67**
2. proper-motion diagram, cluster the stars in (pmra, pmdec, parallax) with DBSCAN
3. members → distance from the median parallax
4. colour–magnitude (HR) diagram per cluster, `M_G` from the distance modulus
5. turn-off colour → the three clusters ordered by age

## Result (verified)

| cluster  | members | parallax [mas] | distance [pc] | literature | turn-off BP−RP | lit. age |
|----------|--------:|---------------:|--------------:|-----------:|---------------:|---------:|
| Pleiades |     504 |          7.363 |           136 |     136 pc |          −0.05 |  125 Myr |
| Praesepe |     365 |          5.398 |           185 |     186 pc |           0.23 |  700 Myr |
| M67      |     981 |          1.153 |           867 |     ~850 pc |          0.63 |    4 Gyr |

The turn-off colour increases monotonically with age, so the age *ordering* falls
out of the data — no isochrones needed. M67's CMD also shows the red giant branch.

Runtime: **~45 s** from scratch, ~3 s from the on-disk cache. Figure: `clusters.png`.

## Two traps the students (and the agent) will hit

1. **The full `gaiadr3.gaia_source` table times out.** The ESA archive is being
   reworked ahead of DR4 and a 1.5° cone search on the main table died after 61 s
   for me. `Gaia.MAIN_GAIA_TABLE = "gaiadr3.gaia_source_lite"` with
   `cone_search_async` returns 27 000 rows in 10 s. VizieR (`I/355/gaiadr3`) is a
   second fallback, 2 s.
2. **DBSCAN finds the Galactic field, not the cluster.** The biggest clump in
   (pm, parallax) space is the background. My first run put the Pleiades at
   2.1 kpc with 7000 "members". The fix is one line: among the clumps, take the
   *nearest* one (largest median parallax), not the biggest. Worth showing in
   the lecture — it is a perfect example of a confident, plausible, wrong answer.

Smaller things: cut on `parallax_over_error > 10` before clustering, and remember
`M_G = G − 5·log10(d/10 pc)`.

## Optional extension

Isochrone fitting needs an external grid (PARSEC / MIST), which is a manual
download and its own half hour — leave it as a bonus, not as part of the 40 min.
