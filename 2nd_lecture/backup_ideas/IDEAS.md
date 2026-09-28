# Backup project ideas (not on the slides)

Kept for later semesters or for students who finish the cluster project early.

## 1. Spectra: lines and redshift  — TESTED, works

`spectra/spectrum.py` — SDSS spectrum of **NGC 1068 (M77)**, plate 1070, MJD 52591,
fiber 72, fetched with `astroquery.sdss`. Fits Gaussians to Hβ, [O III] 4959/5007,
[O I] 6300, Hα, [N II] 6583, [S II] 6716/6731, labels them on the spectrum and
derives the redshift line by line.

Verified result: z = 0.00427 ± 0.00010 against the SDSS pipeline value 0.00421.
Runtime **5 s**. Figure: `spectra/spectrum.png`.

The teaching point survived the test: using *air* rest wavelengths instead of
*vacuum* ones shifts the answer by **83 km/s**, which is 8× the scatter between
lines. SDSS wavelengths are already vacuum and heliocentric.

Candidates checked for line strength (Hα / continuum): NGC 1068 = 13 (best),
IC 2497 = 3.3, NGC 4102 = 2.0, NGC 4151 = 1.4 (the fiber sits 19" off the
nucleus), M82 = spectrum not retrievable. Use NGC 1068.

## 2. Time series: measure the period — NOT tested

`lightkurve` light curves of RR Lyr (pulsator), δ Cep (Cepheid) and Kepler-10
(transits): flatten, Lomb–Scargle for the pulsators, BLS for the transit,
phase-fold, compare the periods with the catalogue. Kepler-10b is a 150 ppm
transit, so a deeper target (Kepler-8 b, HAT-P-7 b) is the safer choice if this
is ever used.

## 3. Single-cluster version of the Gaia project

The membership half of `project_open_clusters` on its own (one cluster, sky map +
proper-motion diagram + membership probabilities from a Gaussian mixture) is
about half the work, if 40 minutes turns out to be tight.
