"""Schematic figures for lecture 2 (Models, pricing, routing).

Run once to (re)generate all `fig_*.png` used by 02_models_and_routing.ipynb:

    python3 make_figures.py

Same hand-drawn schematic style as 1st_lecture/make_figures.py - no real data.
"""

import os

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

# ----------------------------------------------------------------------
# palette (same as lecture 1)
# ----------------------------------------------------------------------
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#9b9a92"
LINE = "#d8d7d1"

BLUE = "#2a78d6"
ORANGE = "#eb6834"
AQUA = "#1baf7a"
YELLOW = "#eda100"
MAGENTA = "#e87ba4"
VIOLET = "#4a3aa7"
RED = "#e34948"

plt.rcParams.update(
    {
        "figure.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
        "savefig.dpi": 200,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.22,
        "font.family": "DejaVu Sans",
        "text.color": INK,
    }
)


def tint(color, t=0.88):
    c = np.array(to_rgb(color))
    return tuple(c * (1 - t) + t)


def canvas(w, h):
    """Axes with square data units: x in [0, 100], y in [0, 100*h/w]."""
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100 * h / w)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, label="", color=BLUE, face=None, fs=9.5, lw=1.8,
        r=0.8, weight="normal", tc=None, ls="solid", zorder=2):
    ax.add_patch(
        FancyBboxPatch(
            (x, y), w, h,
            boxstyle=f"round,pad=0,rounding_size={r}",
            linewidth=lw, edgecolor=color,
            facecolor=tint(color) if face is None else face,
            linestyle=ls, zorder=zorder,
        )
    )
    if label:
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
                fontsize=fs, color=tc or INK, zorder=zorder + 1,
                linespacing=1.35, weight=weight)
    return x + w / 2, y + h / 2


def arrow(ax, p1, p2, color=INK2, lw=1.6, rad=0.0, ls="solid", zorder=1):
    ax.add_patch(
        FancyArrowPatch(
            p1, p2, arrowstyle="-|>", mutation_scale=11,
            linewidth=lw, color=color, linestyle=ls,
            connectionstyle=f"arc3,rad={rad}",
            shrinkA=1.5, shrinkB=1.5, zorder=zorder,
        )
    )


def title(ax, text, sub=None):
    top = ax.get_ylim()[1]
    ax.text(0, top - 1.2, text, ha="left", va="top", fontsize=12.5, weight="bold", color=INK)
    if sub:
        ax.text(0, top - 4.4, sub, ha="left", va="top", fontsize=9.5, color=INK2)


def save(fig, name):
    fig.savefig(name)
    plt.close(fig)
    print("wrote", name)


# ======================================================================
# 1. model routing ("Auto")
# ======================================================================
def fig_model_routing():
    fig, ax = canvas(11, 3.45)
    top = ax.get_ylim()[1]

    ys = [3.2, 12.4, 21.6]          # bottom edges of the three tiers
    bx, bw, bh = 46.0, 27.0, 8.0
    yc = (ys[0] + ys[-1] + bh) / 2

    # you / your prompt
    box(ax, 1.0, yc - 4.0, 14.5, 8.0, "your\nprompt", color=INK2, face=SURFACE,
        fs=9.5, weight="bold")
    arrow(ax, (15.7, yc), (21.3, yc))

    # the router
    box(ax, 21.5, yc - 5.5, 15.0, 11.0, "", color=ORANGE)
    ax.text(29.0, yc + 1.8, "router", fontsize=10.5, weight="bold", ha="center", va="center")
    ax.text(29.0, yc - 2.4, "a cheap classifier,\nnot the model itself", fontsize=7.6,
            color=INK2, ha="center", va="center", linespacing=1.5)

    # what the router goes on
    ax.text(29.0, 1.6,
            "it decides before anyone has thought about your problem,\n"
            "from prompt length, attached files, task type, server load, your quota",
            fontsize=7.8, color=INK2, ha="center", va="center", linespacing=1.6)
    arrow(ax, (29.0, 3.6), (29.0, yc - 5.9), color=YELLOW)

    # the model tiers
    tiers = [
        ("small & fast", "Haiku, mini models", AQUA,
         "rename, docstring, commit message", "0\u00d7  (included)"),
        ("mid-tier workhorse", "Sonnet, GPT-5", BLUE,
         "most coding turns", "\u2248 1\u00d7"),
        ("frontier / reasoning", "Opus, GPT-5 high effort", VIOLET,
         "hard debugging, design,\nplanning a refactor", "\u2248 5\u201310\u00d7"),
    ]
    for (name, models, c, use, cost), y in zip(tiers, ys):
        box(ax, bx, y, bw, bh, "", color=c)
        ax.text(bx + 2.2, y + bh - 2.6, name, fontsize=9.4, weight="bold", color=INK, va="center")
        ax.text(bx + 2.2, y + 2.6, models, fontsize=8.2, color=c, va="center")
        arrow(ax, (36.7, yc), (bx - 0.5, y + bh / 2), color=c, rad=-0.10)
        ax.text(bx + bw + 2.0, y + bh / 2 + 1.7, use, fontsize=8.0, color=INK2,
                va="center", ha="left", linespacing=1.5)
        ax.text(bx + bw + 2.0, y + bh / 2 - 2.6, cost, fontsize=8.4, color=c,
                va="center", ha="left", weight="bold")

    ax.text(bx + bw + 2.0, ys[-1] + bh + 0.9, "what it costs you", fontsize=8.0,
            color=MUTED, va="bottom", ha="left")

    save(fig, "fig_model_routing.png")


# ======================================================================
# 2. when to let Auto decide, and when not to
# ======================================================================
def fig_auto_vs_manual():
    fig, ax = canvas(11, 4.1)
    top = ax.get_ylim()[1]

    axis_y = 5.5
    x_lo, x_hi = 2.0, 98.0

    tasks = [
        (8.0, "rename a\nvariable", AQUA, 0),
        (22.0, "write a\ndocstring", AQUA, 1),
        (36.0, "add a\nunit test", BLUE, 0),
        (50.0, "port a script\nto numpy", BLUE, 1),
        (64.0, "fix a bug you\ncan reproduce", BLUE, 0),
        (78.0, "design the whole\nanalysis pipeline", VIOLET, 1),
        (92.0, "wrong number,\nno error message", VIOLET, 0),
    ]
    bw, bh = 13.5, 7.6
    rows = [10.5, 20.0]
    for x, label, c, row in tasks:
        y = rows[row]
        box(ax, x - bw / 2, y, bw, bh, label, color=c, fs=7.9)
        ax.plot([x, x], [y, axis_y + 0.6], color=c, lw=1.0, zorder=0)
        ax.plot([x], [axis_y], marker="o", ms=4.0, color=c, zorder=3)

    ax.annotate("", xy=(x_hi, axis_y), xytext=(x_lo, axis_y),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.3, shrinkA=0, shrinkB=0))
    ax.text(x_lo, axis_y - 2.2, "mechanical, verifiable in one glance", fontsize=8.4,
            color=INK2, ha="left", va="top")
    ax.text(x_hi, axis_y - 2.2, "open-ended, expensive to get wrong", fontsize=8.4,
            color=INK2, ha="right", va="top")
    ax.text((x_lo + x_hi) / 2, axis_y - 2.2, "task difficulty  →", fontsize=8.8,
            color=MUTED, ha="center", va="top")

    band_y = 32.5
    bands = [
        (x_lo, 71.0, AQUA, "let Auto pick", "cheap, fast, and a wrong answer costs you one minute"),
        (71.0, x_hi, VIOLET, "pick the strongest model yourself",
         "planning and hard bugs: you will never one-shot these"),
    ]
    for x1, x2, c, name, note in bands:
        ax.plot([x1, x2], [band_y, band_y], color=c, lw=2.2, solid_capstyle="butt")
        for xe in (x1, x2):
            ax.plot([xe, xe], [band_y - 1.1, band_y + 1.1], color=c, lw=2.2)
        ax.text((x1 + x2) / 2, band_y + 2.0, name, fontsize=9.4, weight="bold",
                color=c, ha="center", va="bottom")
        ax.text((x1 + x2) / 2, band_y - 2.0, note, fontsize=8.2, color=INK2,
                ha="center", va="top")

    save(fig, "fig_auto_vs_manual.png")


# ======================================================================
# 3. planning vs. one-shotting
# ======================================================================
def fig_plan_vs_oneshot():
    fig, ax = canvas(11, 3.8)
    top = ax.get_ylim()[1]

    # ---------------- one shot ----------------
    ax.text(0, top - 0.8, "one shot", fontsize=10.5, weight="bold", color=RED,
            ha="left", va="top")
    ax.text(15.0, top - 1.3, "one prompt, one answer \u2014 and no way to see where it broke",
            fontsize=8.6, color=INK2, ha="left", va="top")

    ya, h = 23.0, 8.0
    box(ax, 2.0, ya, 24.0, h, "one long prompt", color=INK2, face=SURFACE, fs=9.2, weight="bold")
    box(ax, 32.0, ya, 26.0, h, "500 lines at once", color=BLUE, fs=9.2)
    box(ax, 64.0, ya, 26.0, h, "something is wrong", color=RED, fs=9.2)
    arrow(ax, (26.3, ya + h / 2), (31.7, ya + h / 2))
    arrow(ax, (58.3, ya + h / 2), (63.7, ya + h / 2), color=RED)

    fb = 20.2
    ax.plot([77.0, 77.0], [ya, fb], color=RED, lw=1.4, zorder=0)
    ax.plot([77.0, 14.0], [fb, fb], color=RED, lw=1.4, zorder=0)
    arrow(ax, (14.0, fb), (14.0, ya - 0.2), color=RED, lw=1.4)
    ax.text(45.5, 18.8, "start over", fontsize=8.8, color=RED, ha="center", va="center")

    ax.plot([0, 100], [16.8, 16.8], color=LINE, lw=1.2)

    # ---------------- plan first ----------------
    ax.text(0, 15.8, "plan first", fontsize=10.5, weight="bold", color=AQUA,
            ha="left", va="top")
    ax.text(17.0, 15.3, "one prompt for the plan, then one small prompt per step",
            fontsize=8.6, color=INK2, ha="left", va="top")

    yb = 4.5
    box(ax, 2.0, yb, 24.0, h, "a written plan:\nnumbered steps", color=AQUA, fs=9.0)
    for i in range(3):
        x = 32.0 + i * 18.0
        box(ax, x, yb, 15.0, h, f"step {i + 1}", color=BLUE, fs=9.0)
        ax.text(x + 7.5, yb - 2.2, "check it", fontsize=7.8, color=AQUA,
                ha="center", va="center")
        arrow(ax, (x - 2.7, yb + h / 2), (x - 0.3, yb + h / 2))
    box(ax, 86.0, yb, 12.0, h, "it works", color=AQUA, fs=9.0, weight="bold")
    arrow(ax, (83.3, yb + h / 2), (85.7, yb + h / 2))

    save(fig, "fig_plan_vs_oneshot.png")


# ======================================================================
# 4. anatomy of a prompt
# ======================================================================
def fig_prompt_anatomy():
    fig, ax = canvas(11, 3.4)
    top = ax.get_ylim()[1]

    # ---------------- vague ----------------
    ax.text(1.5, top - 1.0, "vague", fontsize=10.5, weight="bold", color=RED,
            ha="left", va="top")
    box(ax, 1.5, top - 12.0, 36.0, 7.5, "", color=RED)
    ax.text(3.5, top - 8.2, "fix the plotting, it doesn't work", fontsize=8.8,
            family="monospace", color=INK, ha="left", va="center")

    bad = [
        "which file?  which plot?",
        "\u201cdoesn't work\u201d \u2014 no error text",
        "so it guesses: four files edited,\nall of them confidently",
    ]
    y = top - 15.5
    for b in bad:
        ax.text(2.0, y, "\u2717", fontsize=9, color=RED, ha="left", va="top")
        ax.text(5.0, y, b, fontsize=8.4, color=INK2, ha="left", va="top", linespacing=1.6)
        y -= 4.2 if "\n" not in b else 6.6

    ax.plot([40.0, 40.0], [1.0, top - 1.5], color=LINE, lw=1.2)

    # ---------------- specific ----------------
    ax.text(43.0, top - 1.0, "specific", fontsize=10.5, weight="bold", color=AQUA,
            ha="left", va="top")

    cx, cw = 43.0, 40.0
    ch = 20.5
    cy = top - 6.0 - ch
    box(ax, cx, cy, cw, ch, "", color=AQUA)

    lines = [
        ("In hr_diagram.py the colour-magnitude plot is empty.", "the file, by name"),
        ("", None),
        ("Traceback: KeyError: 'phot_g_mean_mag', line 42.", "the real error, pasted"),
        ("The csv is a Gaia DR3 gaia_source cone search.", "context it cannot guess"),
        ("", None),
        ("Fix the column lookup. Do not touch the query.", "what must not change"),
    ]
    ly = cy + ch - 2.6
    step = 2.75
    for text, note in lines:
        if text:
            ax.text(cx + 2.2, ly, text, fontsize=7.0, family="monospace",
                    color=INK, ha="left", va="center")
        if note:
            ax.plot([cx + cw + 0.6, cx + cw + 2.2], [ly, ly], color=AQUA, lw=1.0)
            ax.text(cx + cw + 3.0, ly, note, fontsize=7.6, color=AQUA,
                    ha="left", va="center")
        ly -= step

    save(fig, "fig_prompt_anatomy.png")


# ======================================================================
# YouTube channel screenshots for the news slide
#   fireship.png / sentdex.png are manual screenshots of the channel pages;
#   this crops them to their top two rows and writes the JPEGs used by the slide.
# ======================================================================
def crop_screenshots():
    from PIL import Image

    for name, cut in [("fireship", 690), ("sentdex", 655)]:
        src = f"{name}.png"
        if not os.path.exists(src):
            print("skipping", src, "(not here)")
            continue
        im = Image.open(src).convert("RGB")
        w, _ = im.size
        im = im.crop((0, 0, w, cut))
        im = im.resize((1100, round(1100 * cut / w)), Image.LANCZOS)
        im.save(f"{name}_crop.jpg", quality=88, optimize=True)
        print(f"wrote {name}_crop.jpg")


if __name__ == "__main__":
    fig_model_routing()
    # fig_auto_vs_manual()  # kept for reference; merged into the routing slide
    # fig_plan_vs_oneshot()  # kept for reference; merged into the routing slide
    fig_prompt_anatomy()
    crop_screenshots()
