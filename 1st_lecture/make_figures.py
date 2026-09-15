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
    fig, ax = canvas(11, 5.6)
    top = ax.get_ylim()[1]
    title(ax, "A language model does exactly one thing: guess the next token",
          "…and then it does it again, with its own guess appended to the input.")

    toks = ["The", " virial", " theorem", " relates", " kinetic", " and"]
    x = 6.0
    y = top - 15
    for t in toks:
        w = 2.6 + 1.62 * len(t)
        box(ax, x, y, w, 4.4, t.strip(), color=BLUE, fs=9.5)
        x += w + 1.2
    box(ax, x, y, 6.0, 4.4, "?", color=MUTED, face=SURFACE, ls=(0, (3, 2)), fs=11, weight="bold")
    ax.text(6.0, y + 5.6, "the prompt, cut into tokens", fontsize=8.5, color=INK2, va="bottom")

    cx = 50
    arrow(ax, (cx, y - 0.6), (cx, y - 4.2))
    box(ax, 22, y - 11.0, 56, 6.4,
        "transformer:  ~10¹¹ numbers (\"weights\"), fixed after training",
        color=VIOLET, fs=10)
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
# 2. self-attention
# ======================================================================
def fig_attention():
    fig, ax = canvas(11, 3.4)
    top = ax.get_ylim()[1]
    title(ax, "Attention: every word may look back at any earlier word",
          "This replaced reading word-by-word (RNN) in 2017 - the transformer.")

    words = ["The", "cluster", "gas", "is", "hot", "because", "it", "is", "ionized"]
    xs, x = [], 4.0
    y = 17.0
    for w in words:
        bw = 2.6 + 1.62 * len(w)
        box(ax, x, y, bw, 5.0, w, color=BLUE, fs=10)
        xs.append(x + bw / 2)
        x += bw + 1.6

    ax.add_patch(FancyArrowPatch((xs[6], y - 0.4), (xs[1], y - 0.4),
                                 arrowstyle="-|>", mutation_scale=12, linewidth=1.8,
                                 color=ORANGE, connectionstyle="arc3,rad=-0.3", zorder=3))
    ax.text((xs[6] + xs[1]) / 2, y - 11.5, "which \"it\"?  the model looks back at \"cluster\"",
            fontsize=9, color=ORANGE, ha="center")

    ax.text(0, 1.0,
            "Every token looks at every other token, in parallel - which is also why the cost grows "
            "quadratically with context length.",
            fontsize=8.8, color=INK2, ha="left", va="bottom")
    save(fig, "fig_attention.png")


# ======================================================================
# 3. what the model is made of
# ======================================================================
def fig_architecture():
    fig, ax = canvas(11, 3.8)
    top = ax.get_ylim()[1]
    title(ax, "Inside the model: the same block, stacked N times",
          "There is no database and no rulebook in there - only matrices of numbers.")

    yc = 17.0

    box(ax, 1.5, yc - 3.5, 12.5, 7.0, "tokens\n(integers)", color=INK2, face=SURFACE, fs=8.8)
    arrow(ax, (14.4, yc), (17.1, yc))
    box(ax, 17.2, yc - 3.5, 15.0, 7.0, "embedding\ntoken \u2192 vector", color=BLUE, fs=8.8)
    arrow(ax, (32.6, yc), (35.3, yc))

    # the repeated block
    box(ax, 35.5, yc - 8.5, 42.0, 17.0, "", color=VIOLET, face=tint(VIOLET, 0.95))
    ax.text(56.5, yc + 5.6, "transformer block  \u00d7 N", fontsize=9.6, weight="bold",
            color=VIOLET, ha="center", va="center")
    box(ax, 38.0, yc - 6.0, 17.0, 8.5, "self-attention\n(look at other\ntokens)", color=ORANGE, fs=8.2)
    arrow(ax, (55.4, yc - 1.75), (57.6, yc - 1.75))
    box(ax, 58.0, yc - 6.0, 17.0, 8.5, "feed-forward\n(think about\nthis token)", color=AQUA, fs=8.2)

    arrow(ax, (77.9, yc), (80.6, yc))
    box(ax, 80.8, yc - 3.5, 17.7, 7.0, "probability of\nthe next token", color=VIOLET, fs=8.8)

    ax.text(56.5, yc - 10.4,
            "N \u2248 30 - 120 layers; every layer has the same shape but different numbers",
            fontsize=8.4, color=INK2, ha="center", va="top")

    ax.text(0, 1.0,
            "All those numbers together are the parameters (\"weights\"): ~10\u2079 for a model that fits on a "
            "laptop, ~10\u00b9\u00b9 - 10\u00b9\u00b2 for a frontier model.\n"
            "More parameters \u2248 more knowledge and more skill - but also more memory and more compute for "
            "every single token.",
            fontsize=8.8, color=INK2, ha="left", va="bottom", linespacing=1.6)
    save(fig, "fig_architecture.png")


# ======================================================================
# 4. dense vs MoE
# ======================================================================
def fig_dense_vs_moe():
    fig, ax = canvas(11, 4.4)
    top = ax.get_ylim()[1]
    title(ax, "Dense vs. Mixture-of-Experts (MoE)",
          "Two ways to spend parameters. Same number of boxes = same memory; filled boxes = the work actually done per token.")

    def panel(x0, x1, name, active, note, router):
        sq, g = 4.6, 1.0
        gw = 4 * sq + 3 * g
        content = 8 + 3 + (8.5 + 3 if router else 0) + gw
        sx = x0 + (x1 - x0 - content) / 2
        yc = 22.0
        ax.text((x0 + x1) / 2, 29.5, name, fontsize=10.5, weight="bold", ha="center", color=INK)

        box(ax, sx, yc - 2.5, 8, 5, "token", color=INK2, face=SURFACE, fs=8.8)
        cur = sx + 8
        arrow(ax, (cur, yc), (cur + 3, yc))
        cur += 3
        if router:
            box(ax, cur, yc - 2.5, 8.5, 5, "router", color=ORANGE, fs=8.8)
            cur += 8.5
        gx = cur + (3 if router else 0)
        gy = yc - (2 * sq + g) / 2
        for i in range(8):
            r, c = divmod(i, 4)
            on = i in active
            box(ax, gx + c * (sq + g), gy + (1 - r) * (sq + g), sq, sq, "",
                color=BLUE if on else LINE, face=BLUE if on else SURFACE, lw=1.5, r=0.5)
        if router:
            arrow(ax, (cur, yc), (gx - 0.4, yc), color=ORANGE)
        ax.text((x0 + x1) / 2, 13.5, note, fontsize=8.8, color=INK2, ha="center",
                va="top", linespacing=1.6)

    panel(1, 47, "Dense", set(range(8)),
          "every block runs for every token\ncompute per token = 8 / 8", router=False)
    panel(53, 99, "Mixture-of-Experts", {1, 6},
          "a router wakes 2 of the 8 experts\ncompute per token = 2 / 8", router=True)

    ax.plot([50, 50], [8, 31], color=LINE, lw=1.2)
    ax.text(50, 1.0,
            "MoE gives you the knowledge of a huge model at the running cost of a small one — which is why "
            "\"400B parameters\" and \"fast and cheap\" can be true at once.",
            fontsize=8.8, color=INK2, ha="center", va="bottom")
    save(fig, "fig_dense_vs_moe.png")


# ======================================================================
# 4. the context window
# ======================================================================
def fig_context_window():
    fig, ax = canvas(11, 4.4)
    top = ax.get_ylim()[1]
    title(ax, "The context window: everything the model can see, right now",
          "One API call = one flat pile of tokens. There is no memory anywhere else.")

    segs = [
        ("system prompt\n& rules", 7, BLUE),
        ("tool\ndefinitions", 9, ORANGE),
        ("retrieved docs\n(RAG)", 13, AQUA),
        ("your code, files & conversation so far", 34, YELLOW),
        ("room for\nthe answer", 12, MAGENTA),
        ("still free", 25, None),
    ]
    x0, y0, h, wtot = 4.0, 18.0, 8.0, 92.0
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

    ax.annotate("", xy=(x0, 9.5), xytext=(x0 + wtot, 9.5),
                arrowprops=dict(arrowstyle="<|-|>", color=MUTED, lw=1.2, shrinkA=0, shrinkB=0))
    ax.text(50, 8.5, "the whole context window  —  today typically 10⁵ – 10⁶ tokens",
            fontsize=9, color=INK2, ha="center", va="top")

    ax.text(50, 1.0,
            "Anything you did not put in here does not exist for the model: not your last chat, not the file you "
            "did not open, not yesterday's result.\nFilling it well is the whole game — that is what \"context "
            "engineering\" means. Filling it with junk makes answers worse, not better.",
            fontsize=8.8, color=INK2, ha="center", va="bottom", linespacing=1.6)
    save(fig, "fig_context_window.png")


# ======================================================================
# 5. RAG
# ======================================================================
def fig_rag():
    fig, ax = canvas(11, 3.5)
    top = ax.get_ylim()[1]
    title(ax, "RAG — Retrieval-Augmented Generation",
          "The model never learns your papers. You look up the relevant pages and paste them in.")

    y = 5.5
    box(ax, 1.5, y + 10.5, 30, 6.5, "your PDFs, notes, code\n→ chunks → vectors  (once)", color=AQUA, fs=8.8)

    box(ax, 1.5, y, 20, 7.0, "your question", color=INK2, face=SURFACE, fs=9.5)
    box(ax, 26.0, y, 24, 7.0, "search the vectors\n→ best few chunks", color=BLUE, fs=9)
    box(ax, 55.0, y, 22, 7.0, "question\n+ those chunks", color=VIOLET, fs=9)
    box(ax, 81.5, y, 17, 7.0, "LLM → answer\n+ sources", color=VIOLET, fs=9)

    arrow(ax, (21.9, y + 3.5), (25.6, y + 3.5))
    arrow(ax, (50.4, y + 3.5), (54.6, y + 3.5))
    arrow(ax, (77.4, y + 3.5), (81.1, y + 3.5))
    arrow(ax, (31.9, y + 11.0), (38.0, y + 7.6), color=AQUA, ls=(0, (4, 2)))

    ax.text(0, 1.0,
            "For prose (papers, manuals) this is the standard trick. For code, an agent with grep and git "
            "usually beats it.",
            fontsize=8.8, color=INK2, ha="left", va="bottom")
    save(fig, "fig_rag.png")


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

    tools = ["read & edit files", "run shell commands", "run tests, make plots", "search the web", "MCP servers"]
    tw = 17.4
    ty = 3.0
    for i, t in enumerate(tools):
        x = 1.5 + i * (tw + 1.4)
        box(ax, x, ty, tw, 6.2, t, color=ORANGE, fs=8.2)
        ax.plot([x + tw / 2, x + tw / 2], [ty + 6.2, ty + 8.6], color=ORANGE, lw=1.3, zorder=0)
    ax.plot([1.5 + tw / 2, 1.5 + 4 * (tw + 1.4) + tw / 2], [ty + 8.6, ty + 8.6], color=ORANGE, lw=1.3, zorder=0)
    arrow(ax, (48.0, ty + 8.6), (48.0, hy - 0.4), color=ORANGE)
    ax.text(49.8, ty + 9.3, "tools", fontsize=9, color=ORANGE, ha="left")
    save(fig, "fig_harness.png")


# ======================================================================
# 7. multimodality
# ======================================================================
def fig_multimodal():
    fig, ax = canvas(10, 4.2)
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
    box(ax, 68, top - 26.5, 16, 12.5, "transformer", color=VIOLET, fs=10, weight="bold")
    arrow(ax, (84, top - 20.2), (87, top - 20.2), color=VIOLET)
    box(ax, 87, top - 26.5, 12, 12.5, "text\ncode\nimage\nspeech", color=VIOLET, fs=8.8)

    ax.text(50, 1.0,
            "Practical consequence: you can paste a figure, a screenshot of an error, or a photo of a whiteboard "
            "straight into the prompt.",
            fontsize=9, color=INK2, ha="center", va="bottom")
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
    fig, ax = canvas(11, 4.0)
    top = ax.get_ylim()[1]
    title(ax, "How text becomes tokens",
          "A fixed vocabulary of ~10\u2075 frequent character chunks. Common words are one token; rare words split up.")

    ax.text(1.5, top - 12.0, "your text", fontsize=8.5, color=INK2, va="center")
    box(ax, 16.0, top - 15.0, 62.0, 6.0, "The telescope was pointed at a nearby galaxy.",
        color=INK2, face=SURFACE, fs=10.5)
    arrow(ax, (47.0, top - 15.6), (47.0, top - 19.1))
    ax.text(48.8, top - 17.5, "tokenizer", fontsize=8.5, color=INK2, va="center")

    toks = ["The", "\u00b7telescope", "\u00b7was", "\u00b7pointed", "\u00b7at", "\u00b7a",
            "\u00b7nearby", "\u00b7galaxy", "."]
    ids = [976, 121536, 673, 30082, 540, 261, 19486, 66184, 13]

    x, y = 1.5, top - 27.0
    for t, i in zip(toks, ids):
        bw = 2.4 + 1.5 * len(t)
        box(ax, x, y, bw, 5.2, t, color=BLUE, fs=9)
        ax.text(x + bw / 2, y - 2.2, str(i), fontsize=7.6, color=MUTED, ha="center", va="center")
        x += bw + 0.9
    ax.text(1.5, y + 6.6, "9 tokens   (\u00b7 = a leading space, it belongs to the token)",
            fontsize=8.5, color=INK2, va="bottom")
    ax.text(0, 1.0,
            "Those integers are all the model ever sees \u2014 there are no words, no letters, no meaning below this.\n"
            "English prose: ~4 characters \u2248 1 token (1000 tokens \u2248 750 words). Rare names, other languages, "
            "numbers and code split into many more pieces, so they cost more.",
            fontsize=8.6, color=INK2, ha="left", va="bottom", linespacing=1.6)
    save(fig, "fig_tokens.png")


# ======================================================================
# 9. the agent loop
# ======================================================================
def fig_agent_loop():
    fig, ax = canvas(11, 4.0)
    top = ax.get_ylim()[1]
    title(ax, "An agent = the same LLM, called in a loop, with tools",
          "The model only writes text. The harness is what reads that text and acts on it.")

    y1 = 18.0
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

    ax.text(0, 0.8,
            "This loop usually turns 5-50 times before you see one word of the answer. "
            "That is the whole difference between a chatbot and an agent.",
            fontsize=8.8, color=INK2, ha="left", va="bottom")
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
    fig_attention()
    fig_architecture()
    fig_dense_vs_moe()
    fig_multimodal()
    fig_context_window()
    fig_rag()
    fig_harness()
    fig_agent_loop()
    fig_memory()
    # fig_training_stages()  # kept for reference; training is not covered in lecture 1
