#!/usr/bin/env python3
"""Generate 10,000 samples from N(0, 10^2) and plot their distribution."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


SAMPLE_COUNT = 10_000
MEAN = 0
SIGMA = 10
OUTPUT_PATH = Path("normal_distribution.png")


def main() -> None:
    # Change (or remove) the seed if you want a different reproducible sequence.
    rng = np.random.default_rng(seed=42)
    samples = rng.normal(loc=MEAN, scale=SIGMA, size=SAMPLE_COUNT)

    fig, ax = plt.subplots(figsize=(9, 5.5))
    _, bins, _ = ax.hist(
        samples,
        bins=50,
        density=True,
        color="steelblue",
        edgecolor="white",
        alpha=0.8,
        label="Generated samples",
    )

    x = np.linspace(bins[0], bins[-1], 500)
    normal_density = np.exp(-0.5 * ((x - MEAN) / SIGMA) ** 2) / (SIGMA * np.sqrt(2 * np.pi))
    ax.plot(x, normal_density, color="crimson", linewidth=2, label="N(0, 10²) density")

    ax.set(
        title=f"{SAMPLE_COUNT:,} random numbers from a normal distribution",
        xlabel="Random number",
        ylabel="Probability density",
    )
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUTPUT_PATH, dpi=160)
    print(f"Saved plot to {OUTPUT_PATH.resolve()}")
    print(f"Sample mean: {samples.mean():.3f}; sample standard deviation: {samples.std(ddof=1):.3f}")


if __name__ == "__main__":
    main()
