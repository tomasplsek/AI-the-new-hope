# Course for AI the new hope

In this course, I will show my vibe-coding workflow and introduce tools such as [Warp](https://www.warp.dev/), an AI-powered terminal (similar to Codex CLI), and Github Copilot Chat (VS Code extention). I feel like this combination is currently the best - I haven't used Codex CLI or Claude CLI much, but I feel like they lack many features.

Less control over code, more vibe-coding. -> Warp\
More control over codebase, still lot of AI features. -> VS Code + Copilot

Start project with ChatGPT, then vibe-code with Warp, then finalize with Copilot.

## Warp

- started as a smart terminal - single line completions or simple command generation
- now similar to any other AI-powered CLI (probably even better)
- With Build plan ($20 / month) it is possible to use your own API keys or connect to your own LLM.
  - `Auto-approve` button, `Stop agent` button, give specifying commands

- you can select **different LLM models**
  - token usage is displayed in settings and below each response
  - cost, speed, intelligence
  - auto - responsive vs cost-effective
  - can handle long-term memory - shows how much text is left before summarization

- create profiles
  - select base model, command denylist

- you can attach specific content - blocks, files, folders 

- Multi-modality: can also handle **images** (can look at plots) & **speech** (just a Speech-to-text)

- select current working directory + directory view
  - view & edit files

- Warp can also create & edit files
  - `Accept`, `Refine`, `Edit` buttons
  - thumbs up / down for feedback, fork conversation
  - `Review code` button

- bash commands and / commands
  - Agent vs Terminal vs Auto mode
  - /index to index codebase or /new-conversation

- Warp shell includes startup files like .bashrc (unlike Codex CLI)

- display **environments** and **git changes**

- can handle **SSH** - last time there were issues with file editing

- newly can handle interactive terminal **full screen apps** (REPL)
  - `Take over` button

- Workflows & Notebooks - chain commands together
  - `Save as workflow` button

- Rules
  - "Do not use emoji in answers or READMEs."
  - "When you are wrong, do not answer with 'You're absolutely right!'"
  - "Unless specified, do not produce comprehensive project structure, do not turn project into a package or github repo. Do not push anything to github if not asked for."

- MCP servers (Model Context Protocol)
  - agents can basically only run bash commands & edit files
  - to seach web, you can use wget or curl and parse HTML (not very effective)
  - better to use MCP servers (e.g. Brave search)
  - more tools: fetch docummentation, long-term memory, etc.

### MCP Servers
- [Brave search](https://brave.com/search/api/) (`brave_web_search`)
  - "What is the weather forecast for Brno?"

- [ArXiV MCP](https://hub.docker.com/mcp/server/arxiv-mcp-server/overview) (`search_papers`, `download_paper`, `read_paper`)
 - show how to add via docker
  "Give me a list of papers authored by Plšek Tomáš published on arxiv."
  
- [Astro MCP](https://mcpservers.org/servers/SandyYuan/astro_mcp) (`search_objects`, `preview_data`, `astroquery_query`)
  "For the list of galaxies in galaxies.csv, find coordinates and redshifts"
  "Only pick those below redshift of 0.05 and download their SDSS image."

Examples of use:
- You can turn your old PC into Nextcloud server.
- You can turn your old go-pro / web-camera into IP camera.
- You can ALSO fuck-up your server - tried setting CPU quota for each user and but restricted number of all SSH processes to 24 which made the server inaccessible.
- You can use Warp to install MCP server.


