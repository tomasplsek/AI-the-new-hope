"""Schematic figures for lecture 1 (Introduction to AI).

Run once to (re)generate all `fig_*.png` used by 01_introduction.ipynb:

    python3 make_figures.py

Everything here is a hand-drawn schematic - no real data, no network access.
"""

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, to_rgb
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

# ----------------------------------------------------------------------
# palette (validated, colourblind-safe categorical order)
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

BLUES = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#2a78d6", "#256abf", "#184f95", "#0d366b"]

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
# 1. next-token prediction
# ======================================================================
def fig_next_token():
    fig, ax = canvas(11, 5.25)
    top = ax.get_ylim()[1]
    title(ax, "Guessing the next token")

    toks = ["The", " virial", " theorem", " relates", " kinetic", " and"]
    x = 6.0
    y = top - 12
    for t in toks:
        w = 2.6 + 1.62 * len(t)
        box(ax, x, y, w, 4.4, t.strip(), color=BLUE, fs=9.5)
        x += w + 1.2
    box(ax, x, y, 6.0, 4.4, "?", color=MUTED, face=SURFACE, ls=(0, (3, 2)), fs=11, weight="bold")
    ax.text(6.0, y + 5.6, "the prompt, cut into tokens", fontsize=8.5, color=INK2, va="bottom")

    cx = 50
    arrow(ax, (cx, y - 0.6), (cx, y - 4.2))
    box(ax, 38, y - 11.0, 24, 6.4, "LLM", color=VIOLET, fs=13, weight="bold")
    arrow(ax, (cx, y - 11.6), (cx, y - 15.2))

    ax.text(6, y - 16.6, "probability of every possible next token  (~10⁵ candidates)",
            fontsize=9, color=INK2, va="top")

    cands = [("potential", 0.71), ("thermal", 0.11), ("gravitational", 0.06),
             ("magnetic", 0.03), ("all 10⁵ others", 0.09)]
    bx, bw = 26.0, 42.0
    by = y - 19.5
    for i, (name, p) in enumerate(cands):
        yy = by - i * 3.2
        col = BLUE if i < 4 else MUTED
        ax.add_patch(FancyBboxPatch((bx, yy - 2.2), max(bw * p, 0.9), 2.2,
                                    boxstyle="round,pad=0,rounding_size=0.35",
                                    linewidth=0, facecolor=col, zorder=2))
        ax.text(bx - 1.5, yy - 1.1, name, ha="right", va="center", fontsize=9,
                color=INK if i < 4 else INK2)
        ax.text(bx + max(bw * p, 0.9) + 1.5, yy - 1.1, f"{p:.0%}", ha="left",
                va="center", fontsize=8.5, color=INK2)

    ax.text(78, by - 4.0,
            "sampling picks one of them\n(\"temperature\" = how adventurous\nthat pick is; 0 = always the top one)",
            fontsize=8.8, color=INK2, va="center", ha="left", linespacing=1.5)
    arrow(ax, (76.5, by - 4.0), (70.0, by - 4.0))
    save(fig, "fig_next_token.png")


# ======================================================================
# autoregression: the output is fed back in
# ======================================================================
def fig_autoregression():
    fig, ax = canvas(11, 4.0)
    top = ax.get_ylim()[1]
    title(ax, "One token per pass",
          "Each new token is appended to the input, and the whole model runs again \u2014 autoregression.")

    prompt_w = 34.0
    x0 = 13.0
    grown = [("potential", 14.0), ("energy", 10.5), (".", 3.6), ("<end>", 9.0)]

    for row in range(4):
        y = top - 15.0 - row * 6.6
        ax.text(11.0, y + 2.2, f"pass {row + 1}", fontsize=8.5, color=MUTED,
                ha="right", va="center")
        box(ax, x0, y, prompt_w, 4.4, "The virial theorem relates kinetic and",
            color=BLUE, fs=8.6)
        x = x0 + prompt_w + 0.7
        for j in range(row + 1):
            label, w = grown[j]
            new = (j == row)
            col = ORANGE if new else BLUE
            last = (label == "<end>")
            box(ax, x, y, w, 4.4, label, color=MUTED if last else col,
                face=SURFACE if last else None, ls=(0, (3, 2)) if last else "solid",
                fs=8.6, tc=INK2 if last else INK)
            if new:
                ax.plot([x, x + w], [y + 5.2, y + 5.2], color=ORANGE, lw=1.2)
                ax.text(x + w / 2, y + 5.8, "new", fontsize=7.4, color=ORANGE,
                        ha="center", va="bottom")
            x += w + 0.7
        if row == 3:
            ax.text(x + 1.5, y + 2.2, "\u2190 the model asks to stop", fontsize=8.5,
                    color=INK2, ha="left", va="center")

    save(fig, "fig_autoregression.png")


# ======================================================================
# thinking effort
# ======================================================================
def fig_thinking_effort():
    fig, ax = canvas(10, 3.4)
    top = ax.get_ylim()[1]
    title(ax, "Thinking effort",
          "Thinking tokens are just more autoregression \u2014 hidden from you, but billed to you.")

    rows = [("low", 7.0, "~10\u00b2"), ("medium", 21.0, "~10\u00b3"), ("high", 42.0, "~10\u2074")]
    x0, pw, aw, h = 16.0, 12.0, 13.0, 5.0
    for i, (name, tw, n) in enumerate(rows):
        y = 18.0 - i * 8.0
        ax.text(x0 - 1.5, y + h / 2, name, fontsize=9, color=INK2, ha="right", va="center")
        box(ax, x0, y, pw, h, "prompt", color=BLUE, fs=8.4)
        tx = x0 + pw + 0.6
        box(ax, tx, y, tw, h, "thinking" if tw > 12 else "", color=ORANGE, fs=8.4)
        ax.text(tx + tw / 2, y - 1.2, f"{n} thinking tokens", fontsize=8.0, color=ORANGE,
                ha="center", va="top")
        box(ax, tx + tw + 0.6, y, aw, h, "answer", color=VIOLET, fs=8.4)
    save(fig, "fig_thinking_effort.png")






# ======================================================================
# 4. dense vs MoE
# ======================================================================
def fig_dense_vs_moe():
    fig, ax = canvas(11, 4.5)
    top = ax.get_ylim()[1]
    title(ax, "Dense vs. Mixture-of-Experts (MoE)",
          "Each column is one layer, each box one expert. Same number of boxes = same memory; "
          "filled boxes = the work actually done for one token.")

    ROWS, COLS = 5, 4
    sq, gx_, gy_ = 3.6, 3.2, 0.9
    gw = COLS * sq + (COLS - 1) * gx_
    gh = ROWS * sq + (ROWS - 1) * gy_
    yc = 19.3

    def panel(x0, x1, name, active, note, router):
        content = 7 + 2.5 + 8 + 2.5 + gw
        sx = x0 + (x1 - x0 - content) / 2
        gy = yc - gh / 2
        gx = sx + content - gw
        ax.text((x0 + x1) / 2, 32.3, name, fontsize=10.5, weight="bold", ha="center", color=INK)

        box(ax, sx, yc - 2.5, 7, 5, "token", color=INK2, face=SURFACE, fs=8.6)
        if router:
            arrow(ax, (sx + 7, yc), (sx + 9.5, yc))
            box(ax, sx + 9.5, yc - 2.5, 8, 5, "router", color=ORANGE, fs=8.6)
            arrow(ax, (sx + 17.5, yc), (gx - 0.4, yc), color=ORANGE)
        else:
            arrow(ax, (sx + 7, yc), (gx - 0.4, yc))

        def cx(c):
            return gx + c * (sq + gx_)

        def cy(r):
            return gy + (ROWS - 1 - r) * (sq + gy_)

        lcol, lw = (BLUE, 1.3) if router else (LINE, 0.5)
        for r in active[0]:
            ax.plot([gx - 0.4, cx(0)], [yc, cy(r) + sq / 2], color=lcol, lw=lw, zorder=1)
        for c in range(COLS - 1):
            for r1 in active[c]:
                for r2 in active[c + 1]:
                    ax.plot([cx(c) + sq, cx(c + 1)], [cy(r1) + sq / 2, cy(r2) + sq / 2],
                            color=lcol, lw=lw, zorder=1)

        for c in range(COLS):
            for r in range(ROWS):
                on = r in active[c]
                box(ax, cx(c), cy(r), sq, sq, "",
                    color=BLUE if on else LINE, face=BLUE if on else SURFACE,
                    lw=1.4, r=0.5, zorder=2)

        ax.text((x0 + x1) / 2, 6.2, note, fontsize=8.8, color=INK2, ha="center",
                va="top", linespacing=1.6)

    dense = [list(range(ROWS))] * COLS
    moe = [[1, 3], [0, 2], [2, 4], [1, 3]]
    panel(1, 47, "Dense", dense,
          "every expert runs in every layer\ncompute per token = 20 / 20", router=False)
    panel(53, 99, "Mixture-of-Experts", moe,
          "a router wakes 2 of the 5 experts in each layer\ncompute per token = 8 / 20", router=True)

    ax.plot([50, 50], [4.0, 33.8], color=LINE, lw=1.2)
    save(fig, "fig_dense_vs_moe.png")


# ======================================================================
# 4. the context window
# ======================================================================
def fig_context_window():
    fig, ax = canvas(11, 3.55)
    top = ax.get_ylim()[1]
    title(ax, "The context window: everything the model can see, right now")

    segs = [
        ("system prompt\n& rules", 7, BLUE),
        ("tool\ndefinitions", 9, ORANGE),
        ("retrieved docs\n(RAG)", 13, AQUA),
        ("your code, files & conversation so far", 34, YELLOW),
        ("room for\nthe answer", 12, MAGENTA),
        ("still free", 25, None),
    ]
    x0, y0, h, wtot = 4.0, 13.5, 8.0, 92.0
    gap = 0.45
    x = x0
    for i, (name, share, col) in enumerate(segs):
        w = wtot * share / 100 - gap
        if col is None:
            box(ax, x, y0, w, h, "", color=LINE, face=SURFACE, lw=1.4)
            ax.text(x + w / 2, y0 + h / 2, "still free", fontsize=9, color=MUTED,
                    ha="center", va="center")
        else:
            box(ax, x, y0, w, h, "", color=col, face=col, lw=0)
            up = i % 2 == 0
            ax.plot([x + w / 2, x + w / 2],
                    [y0 + h, y0 + h + 1.6] if up else [y0, y0 - 1.6], color=MUTED, lw=1.0)
            ax.text(x + w / 2, y0 + h + 2.0 if up else y0 - 2.0, name, fontsize=8.8,
                    color=INK, ha="center", va="bottom" if up else "top", linespacing=1.4)
        x += w + gap

    ax.annotate("", xy=(x0, 4.6), xytext=(x0 + wtot, 4.6),
                arrowprops=dict(arrowstyle="<|-|>", color=MUTED, lw=1.2, shrinkA=0, shrinkB=0))
    ax.text(50, 3.6, "the whole context window  —  today typically 272 K or 1 M tokens",
            fontsize=9, color=INK2, ha="center", va="top")

    save(fig, "fig_context_window.png")




# ======================================================================
# 6. harness
# ======================================================================
def fig_harness():
    fig, ax = canvas(11, 4.0)
    top = ax.get_ylim()[1]
    title(ax, "The harness: the program that turns a chat model into a coding agent",
          "Codex CLI, Claude Code, Copilot, Cursor… You rent the model; the harness is what you install.")

    hy, hh = 13.5, 14.5
    box(ax, 20.0, hy, 56.0, hh, "", color=BLUE, face=tint(BLUE, 0.95))
    ax.text(22.5, hy + hh - 2.6, "harness", fontsize=10.5, weight="bold", color=BLUE, va="center")

    inner = [("builds the context", BLUE), ("declares the tools", ORANGE),
             ("runs the loop", AQUA), ("keeps memory", MAGENTA)]
    iw, ig = 12.0, 1.6
    for i, (lab, c) in enumerate(inner):
        box(ax, 22.5 + i * (iw + ig), hy + 2.2, iw, 6.8, lab.replace(" ", "\n", 1), color=c, fs=8.4)

    box(ax, 1.5, hy + 3.0, 13.0, 8.5, "you", color=INK2, face=SURFACE, fs=10, weight="bold")
    arrow(ax, (14.9, hy + 7.2), (19.6, hy + 7.2))
    box(ax, 82.0, hy + 3.0, 16.5, 8.5, "LLM\n(API)", color=VIOLET, fs=10, weight="bold")
    arrow(ax, (76.4, hy + 9.0), (81.6, hy + 9.0))
    arrow(ax, (81.6, hy + 5.5), (76.4, hy + 5.5), color=VIOLET)
    ax.text(79.0, hy + 10.2, "prompt", fontsize=8.0, color=INK2, ha="center")
    ax.text(79.0, hy + 3.4, "answer", fontsize=8.0, color=VIOLET, ha="center")

    tools = ["read & edit files", "run shell commands", "search the web", "MCP servers"]
    tw, tg = 17.4, 1.4
    ty = 3.0
    x0 = (100.0 - (len(tools) * tw + (len(tools) - 1) * tg)) / 2
    for i, t in enumerate(tools):
        x = x0 + i * (tw + tg)
        box(ax, x, ty, tw, 6.2, t, color=ORANGE, fs=8.2)
        ax.plot([x + tw / 2, x + tw / 2], [ty + 6.2, ty + 8.6], color=ORANGE, lw=1.3, zorder=0)
    ax.plot([x0 + tw / 2, x0 + (len(tools) - 1) * (tw + tg) + tw / 2], [ty + 8.6, ty + 8.6],
            color=ORANGE, lw=1.3, zorder=0)
    arrow(ax, (48.0, ty + 8.6), (48.0, hy - 0.4), color=ORANGE)
    ax.text(49.8, ty + 9.3, "tools", fontsize=9, color=ORANGE, ha="left")
    save(fig, "fig_harness.png")


# ======================================================================
# 7. multimodality
# ======================================================================
def fig_multimodal():
    fig, ax = canvas(10, 3.5)
    top = ax.get_ylim()[1]
    title(ax, "Multimodality: it is all tokens in the end",
          "Images, audio and text are each cut into pieces and mapped into the same vector space.")

    ins = [("text\n\"fit this spectrum\"", BLUE), ("image\n(a plot, a screenshot)", ORANGE), ("audio / video", AQUA)]
    for i, (t, c) in enumerate(ins):
        y = top - 15 - i * 8.0
        box(ax, 1.5, y, 21, 6.6, t, color=c, fs=8.8)
        arrow(ax, (22.5, y + 3.3), (28.5, y + 3.3), color=c)
        box(ax, 28.5, y, 13, 6.6, "encoder", color=c, fs=8.8)
        arrow(ax, (41.5, y + 3.3), (48.0, top - 20.2), color=c, rad=0.0)

    box(ax, 48, top - 26.5, 16, 12.5, "one shared\nsequence of\ntokens", color=VIOLET, fs=9)
    arrow(ax, (64, top - 20.2), (68, top - 20.2), color=VIOLET)
    box(ax, 68, top - 26.5, 16, 12.5, "LLM", color=VIOLET, fs=11, weight="bold")
    arrow(ax, (84, top - 20.2), (87, top - 20.2), color=VIOLET)
    box(ax, 87, top - 26.5, 12, 12.5, "text\ncode\nimage\nspeech", color=VIOLET, fs=8.8)

    save(fig, "fig_multimodal.png")


# ======================================================================
# 8. how a model is made
# ======================================================================
def fig_training_stages():
    fig, ax = canvas(11, 3.4)
    top = ax.get_ylim()[1]
    title(ax, "How a model is made — and where you come in")

    stages = [
        ("pre-training", "predict the next token\non ~everything written\n\nmonths, 10⁴ GPUs", BLUE),
        ("fine-tuning (SFT)", "imitate good answers\nwritten by humans\n\ndays", ORANGE),
        ("RL post-training", "reward what people prefer\nand what is verifiably right\n(→ \"reasoning\" models)", AQUA),
        ("you, at runtime", "prompt, context, tools,\nagent loop\n\nseconds", VIOLET),
    ]
    w, h, gap = 21.5, 15.5, 4.0
    y = top - 22.5
    for i, (name, body, c) in enumerate(stages):
        x = 1.5 + i * (w + gap)
        box(ax, x, y, w, h, "", color=c, fs=9)
        ax.text(x + w / 2, y + h - 3.0, name, fontsize=9.8, weight="bold", ha="center", va="center", color=INK)
        ax.text(x + w / 2, y + h / 2 - 2.2, body, fontsize=8.3, ha="center", va="center",
                color=INK2, linespacing=1.55)
        if i:
            arrow(ax, (x - gap + 0.4, y + h / 2), (x - 0.4, y + h / 2))

    x_end = 1.5 + 2 * (w + gap) + w
    ax.plot([1.5, x_end], [y - 2.5, y - 2.5], color=MUTED, lw=1.2)
    ax.text((1.5 + x_end) / 2, y - 4.0, "the weights change — done by the lab, costs $10⁷–10⁹",
            fontsize=8.6, color=INK2, ha="center", va="top")
    x4 = 1.5 + 3 * (w + gap)
    ax.plot([x4, x4 + w], [y - 2.5, y - 2.5], color=VIOLET, lw=1.2)
    ax.text(x4 + w / 2, y - 4.0, "weights frozen —\nonly the input changes",
            fontsize=8.6, color=VIOLET, ha="center", va="top", linespacing=1.5)
    save(fig, "fig_training_stages.png")


# ======================================================================
# how text becomes tokens
# ======================================================================
def fig_tokens():
    fig, ax = canvas(11, 3.45)
    top = ax.get_ylim()[1]
    title(ax, "How text becomes tokens",
          "A fixed vocabulary of ~10\u2075 frequent character chunks. Common words are one token; rare words split up.")

    ax.text(1.5, top - 12.0, "your text", fontsize=8.5, color=INK2, va="center")
    box(ax, 16.0, top - 15.0, 62.0, 6.0, "The telescope was pointed at a nearby quasar.",
        color=INK2, face=SURFACE, fs=10.5)
    arrow(ax, (47.0, top - 15.6), (47.0, top - 19.1))
    ax.text(48.8, top - 17.5, "tokenizer", fontsize=8.5, color=INK2, va="center")

    toks = ["The", "\u00b7telescope", "\u00b7was", "\u00b7pointed", "\u00b7at", "\u00b7a",
            "\u00b7nearby", "\u00b7qu", "asar", "."]
    ids = [976, 121536, 673, 30082, 540, 261, 19486, 474, 50450, 13]
    split = [False] * 7 + [True, True, False]

    x, y = 1.5, top - 27.0
    for t, i, is_split in zip(toks, ids, split):
        bw = 2.2 + 1.45 * len(t)
        c = ORANGE if is_split else BLUE
        box(ax, x, y, bw, 5.2, t, color=c, fs=9)
        ax.text(x + bw / 2, y - 2.2, str(i), fontsize=7.6, color=MUTED, ha="center", va="center")
        x += bw + 0.75
    ax.text(1.5, y + 6.6, "10 tokens   (\u00b7 = a leading space, it belongs to the token)",
            fontsize=8.5, color=INK2, va="bottom")
    ax.text(x - 0.75, y + 6.6, "\u201cquasar\u201d is rare enough that it costs two tokens",
            fontsize=8.5, color=ORANGE, ha="right", va="bottom")
    save(fig, "fig_tokens.png")


# ======================================================================
# 9. the agent loop
# ======================================================================
def fig_agent_loop():
    fig, ax = canvas(11, 3.35)
    top = ax.get_ylim()[1]
    title(ax, "Agent = LLM, called in a loop, with tools")

    y1 = 13.5
    box(ax, 1.5, y1, 12, 7.5, "you", color=INK2, face=SURFACE, fs=10, weight="bold")
    box(ax, 19.5, y1, 21, 7.5, "context\n= everything so far", color=BLUE, fs=9)
    box(ax, 47.0, y1, 12, 7.5, "LLM", color=VIOLET, fs=11, weight="bold")
    box(ax, 70.0, y1 + 4.0, 27, 7.0, "final answer  →  you", color=AQUA, fs=9.5)
    box(ax, 70.0, y1 - 12.0, 27, 7.5, "tool call  →  harness runs it\n(bash, edit file, python)", color=ORANGE, fs=8.8)

    arrow(ax, (13.9, y1 + 3.75), (19.1, y1 + 3.75))
    arrow(ax, (40.9, y1 + 3.75), (46.6, y1 + 3.75))
    arrow(ax, (59.4, y1 + 5.4), (69.6, y1 + 7.5))
    arrow(ax, (59.4, y1 + 2.0), (69.6, y1 - 5.5))
    ax.text(61.0, y1 + 9.4, "done", fontsize=8.4, color=AQUA, ha="left", va="center")
    ax.text(56.5, y1 - 5.0, "needs a tool", fontsize=8.4, color=ORANGE, ha="left", va="center")

    ax.plot([69.6, 30.0, 30.0], [y1 - 8.2, y1 - 8.2, y1 - 2.5], color=ORANGE, lw=1.6,
            zorder=1, solid_capstyle="round")
    arrow(ax, (30.0, y1 - 3.0), (30.0, y1 - 0.3), color=ORANGE)
    ax.text(31.8, y1 - 7.4, "the result is pasted back in",
            fontsize=8.6, color=ORANGE, ha="left", va="bottom")

    save(fig, "fig_agent_loop.png")


# ======================================================================
# 10. memory: what survives what
# ======================================================================
def fig_memory():
    fig, ax = canvas(11, 3.4)
    top = ax.get_ylim()[1]
    title(ax, "What is remembered — and for how long",
          "The weights never change. Anything that feels like memory is a file read back into the context.")

    panels = [
        (BLUE, "one API call", "seconds", "the context window —\ngone when the call returns"),
        (ORANGE, "one session", "hours", "the transcript is re-sent every turn;\nwhen it stops fitting it is summarised"),
        (AQUA, "across sessions", "forever", "only what is on disk:\nAGENTS.md, notes, your repo, an index"),
    ]

    w, h, gap = 30.0, 15.0, 3.5
    y = 8.0
    for i, (c, name, dur, body) in enumerate(panels):
        x = 1.5 + i * (w + gap)
        box(ax, x, y, w, h, "", color=c)
        ax.text(x + w / 2, y + h - 3.2, name, fontsize=10, weight="bold", ha="center", va="center", color=INK)
        ax.text(x + w / 2, y + h - 6.4, dur, fontsize=8.4, ha="center", va="center", color=c)
        ax.text(x + w / 2, y + 4.2, body, fontsize=8.4, ha="center", va="center",
                color=INK2, linespacing=1.6)
        if i:
            arrow(ax, (x - gap + 0.3, y + h / 2), (x - 0.5, y + h / 2))

    ax.text(0, 1.5,
            "If you want the agent to know something tomorrow, it has to end up in a file today.",
            fontsize=8.8, color=INK2, ha="left", va="bottom")
    save(fig, "fig_memory.png")


if __name__ == "__main__":
    fig_tokens()
    fig_next_token()
    fig_autoregression()
    fig_thinking_effort()
    fig_dense_vs_moe()
    fig_multimodal()
    fig_context_window()
    fig_harness()
    fig_agent_loop()
    fig_memory()
    # fig_training_stages()  # kept for reference; training is not covered in lecture 1
