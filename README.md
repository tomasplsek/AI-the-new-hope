# AI: the new hope

A hands-on course at Masaryk University on using large language models and coding
agents for real work in physics and astrophysics. Slides, notebooks and exercises
live here, one folder per lecture.

## Lectures

**1. Introduction** ([`1st_lecture/`](1st_lecture)): tokens, next-token prediction,
dense vs. mixture-of-experts, context window, memory, agents and harnesses; the
OpenAI API from Python; first look at GitHub Copilot.
Notebook: [`01_introduction.ipynb`](1st_lecture/01_introduction.ipynb).

**2. Models, routing and prompting** ([`2nd_lecture/`](2nd_lecture)): where to
follow AI news, what Copilot's *Auto* does, why you plan before you code, and how
to write a prompt worth sending.
Slides: [`2nd_lecture.pdf`](2nd_lecture/2nd_lecture.pdf).

**3. A problem of your own** ([`3rd_lecture/`](3rd_lecture)): one sitting with the
agent on [open clusters in Gaia DR3](3rd_lecture/astro_task.pdf) or on the
[quantum Ising transition](3rd_lecture/theor_problem.pdf).

## Building the material

```bash
python3 1st_lecture/scripts/make_figures.py
cd 2nd_lecture && python3 make_figures.py && weasyprint slides.html 2nd_lecture.pdf
```

[`plan.txt`](plan.txt) is the plan for the rest of the semester.
