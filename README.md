# AI: the new hope

A hands-on course at Masaryk University on using large language models and coding
agents for real research work in physics and astrophysics — not what they are in
principle, but what they get right, what they get wrong, and how to tell the
difference. This repository holds the slides, notebooks and exercises.

## Lectures so far

### 1 — Introduction · [`1st_lecture/`](1st_lecture)

What a model actually is and what happens when you prompt one, presented as a
Jupyter notebook ([`01_introduction.ipynb`](1st_lecture/01_introduction.ipynb)):

- tokens, next-token prediction, autoregression, sampling and thinking effort
- model size, quantization, dense vs. mixture-of-experts
- multimodality; the context window and what falls out of it; memory
- agents = model + tools + a loop, and the harness around them
- the OpenAI API from Python, the playground, and a first look at GitHub Copilot

`figures/` holds the schematics (regenerate with `python3 scripts/make_figures.py`),
`scripts/` the small worked examples used live — parabola fitting, the virial
velocity profile and the white-dwarf mass–radius relation.

### 2 — Models, routing and prompting · [`2nd_lecture/`](2nd_lecture)

Four slides, [`2nd_lecture.pdf`](2nd_lecture/2nd_lecture.pdf):

- where to follow AI news: people worth reading, two newsletters, two benchmark sites
- **model routing** — what Copilot's *Auto* really does, why it is not the same
  router as in a mixture-of-experts model, and when to pick the model yourself;
  plan first, because you will not one-shot a real problem
- **prompting tips** — a vague prompt against a specific one, line by line
- the short projects, one astrophysical and one theoretical

### 3 — A problem of your own · [`3rd_lecture/`](3rd_lecture)

One sitting with the agent on a real problem:
[`astro_task.pdf`](3rd_lecture/astro_task.pdf) — open clusters in Gaia DR3: query
the archive, cluster the stars in proper motion and parallax, pick the members,
build the HR diagrams and order three clusters by age;
[`theor_problem.pdf`](3rd_lecture/theor_problem.pdf) — the quantum Ising phase
transition on a ring, from ferromagnetic order to a quantum paramagnet.

## Building the material

```bash
# lecture 1 — figures for the notebook
python3 1st_lecture/scripts/make_figures.py

# lecture 2 — figures, then the slides
cd 2nd_lecture && python3 make_figures.py && weasyprint slides.html 2nd_lecture.pdf
```

[`plan.txt`](plan.txt) is the running plan for the rest of the semester: tools and
harnesses, local and open-weight models, equation-driven work with Lean, agents
talking to each other, and student projects until the end of term.
