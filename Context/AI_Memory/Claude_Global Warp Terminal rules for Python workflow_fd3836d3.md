---
title: "Global Warp Terminal rules for Python workflow"
date: 2026-05-17T23:40:34.577998Z
tags: [ai_memory, claude_context]
summary: "**Conversation Overview**  The person is working to build and configure global Rules for their Warp Terminal, a developer-focused terminal application that learns user preferences and working styles. They shared two existing Warp-generated rules about their Python version management (using uv and .venv virtual environments, with Python 3.14 globally on both macOS and Windows) and their use of both VSCode and Antigravity as code editors. They asked Claude to expand and improve these rules based on their broader tech stack and working patterns, drawing on skill files that were read during the conversation.  Claude accessed several skill files documenting the person's established standards across data science, web development, and aerospace/robotics engineering domains. From these, Claude synthesized an 11-rule global configuration document covering: Python environment management with uv (improved with explicit command equivalents, initialization sequences, and project-vs-global Python distinctions); editor configuration with VSCode defaults including a `.vscode/settings.json` template; a mandatory static analysis stack (mypy strict → Ruff → Pylance in priority order); a full `pyproject.toml` baseline template; data science toolchain defaults (pandas/polars, gradient boosting benchmarking rule, storage formats); the T3 Stack for web development with TypeScript strict mode and pnpm; Git conventions (Conventional Commits + SemVer); Docker and CI/CD infrastructure defaults; aerospace and rocketry project conventions (safety standards, simulation tools, ROS2, embedded RTOS, mathematical documentation requirements); terminal behavior defaults (bash-first, `set -euo pipefail`, destructive command warnings, macOS-primary/Windows-secondary); and communication style preferences (precise, rationale-driven, no filler, no emojis).  The person's demonstrated preferences include always using uv over pip/conda/pyenv, defaulting to Python 3.12 for project work, enforcing type hints and Google/NumPy docstrings universally, using pathlib over os.path, structured logging over print statements, and benchmarking XGBoost/LightGBM/CatBoost before neural networks on tabular ML problems. Claude noted at the end that Warp's rules editor renders plain text rather than Markdown tables, and offered to reformat the output for direct copy-paste into Warp's UI if needed."
---

### Human
I want to build global Rules for my Warp Terminal. Through my experience, warp has known me and my style of working, which includes my tech stack and way of working and planning projects. So far, this what Warp has build about me:

Rules:

1. User manages multiple Python versions with uv and .venv: User uses uv python to manage multiple Python versions depending on the project, utilizes .venv virtual environments, and keeps the latest global Python 3.14 installed on both Mac and Windows while maintaining necessary Python versions for OS compatibility.

### Assistant
 

### Human
I want to build global Rules for my Warp Terminal. Through my experience, warp has known me and my style of working, which includes my tech stack and way of working and planning projects. So far, this what Warp has build about me:

Rules:

1. User manages multiple Python versions with uv and .venv: User uses uv python to manage multiple Python versions depending on the project, utilizes .venv virtual environments, and keeps the latest global Python 3.14 installed on both Mac and Windows while maintaining necessary Python versions for OS compatibility.
2. User uses both VSCode and Antigravity editors: User uses both VSCode and Antigravity as code editors.

Help me to build global skills so i can add them to my warp environment, based on our current Skills and what you have learned about me so far. And if we can improve the current existing ones, that would be wonderful.



### Assistant
 The user wants to build global Rules for Warp Terminal based on their tech stack and working style. Let me first read the relevant skill files to understand what's already documented, then craft comprehensive Warp Rules.

Let me read the skill files to understand the current state.
```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

Now I have a good understanding of the user's stack and working style. Let me synthesize this into comprehensive Warp Terminal global rules. Warp rules are written in natural language and tell Warp how to behave and assist. They should be concise, actionable, and reflect the user's actual workflow.

Let me think about what Warp global rules cover:
1. Environment & tooling preferences
2. Code quality standards
3. Project initialization patterns
4. Shell/terminal behavior preferences
5. Editor setup
6. Tech stack defaults

The existing Warp rules are:
1. Python version management with uv and .venv
2. Uses both VSCode and Antigravity editors

Let me improve these and add comprehensive rules based on what I know.

I'll create rules covering:
1. Python environment management (improved)
2. Editors (improved - add Pylance for VSCode)
3. Project initialization (data science)
4. Project initialization (web dev)
5. Code quality / linting
6. Git workflow
7. Shell/terminal preferences
8. Infrastructure / deployment
9. Aerospace/rocketry context

Warp rules are plain text, meant to guide Warp's AI and autocomplete behavior. They should be concise, specific, and prescriptive.Now I have a full picture. Let me build the Warp global rules — improving the two existing ones and adding the full set derived from your stack, workflow, and skill files.
```
This block is not supported on your current device yet.
```

Now I have everything I need. Let me produce the full Warp global rules document.
```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

Here is a breakdown of what was built and why.

---

**What's in the document — 11 rules, each serving a distinct purpose:**

**Rules 1 & 2** are direct improvements on your existing Warp rules. Rule 1 now includes the actual `uv` command equivalents (so Warp can autocomplete and suggest them inline), the project initialization sequence, and the distinction between global Python 3.14 and project-pinned 3.12. Rule 2 adds the VSCode-specific defaults (`.vscode/settings.json` template, extension strategy) that were missing.

**Rule 3** codifies the non-negotiable static analysis stack with the exact priority order — mypy strict first, Ruff second, Pylance as additive — and the CI run order. This is what Warp should enforce whenever it helps you initialize or audit a Python project.

**Rule 4** is the `pyproject.toml` template with all tooling sections pre-configured. Having this in Warp rules means you can generate a compliant project config from a prompt without re-specifying preferences each time.

**Rules 5 & 6** capture your two primary domains — data science and web dev — with the full stack decisions already made. Warp AI won't second-guess whether to use `pandas` or `polars`, or which ORM to default to.

**Rule 7** locks in Conventional Commits + SemVer so Warp's git suggestions stay consistent.

**Rule 8** covers Docker and CI patterns at the defaults you actually use.

**Rule 9** is the aerospace/rocketry context — languages, safety standards, simulation tools, ROS2, embedded RTOS constraints, and the mathematical documentation requirement. This is absent from the current Warp rules entirely.

**Rule 10** standardizes terminal behavior: bash-first, `set -euo pipefail`, destructive-command warnings, and macOS-primary/Windows-secondary assumption.

**Rule 11** mirrors the communication style you expect from AI tools: precise, rationale-driven, no filler.

---

**One thing to clarify before you paste this into Warp:** Warp currently supports rules as plain text (it does not render markdown tables in the rules editor). The document is structured in Markdown for readability here, but when pasting into Warp you may want to either paste the raw text as-is (Warp handles it) or split it into individual rules per section using the "+" button. Let me know if you want a version reformatted for direct copy-paste into Warp's UI — one rule per block.

