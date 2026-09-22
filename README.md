# topology-skill

[![Validate](https://github.com/Sisyphe42/topology-skill/actions/workflows/validate.yml/badge.svg)](https://github.com/Sisyphe42/topology-skill/actions/workflows/validate.yml)
[![Release](https://img.shields.io/github/v/release/Sisyphe42/topology-skill)](https://github.com/Sisyphe42/topology-skill/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A portable [Agent Skill](https://agentskills.io/specification) for inspecting a directory or goal, deciding the right topology, and delivering it inline or as an approved persistent artifact.

The skill assumes a blank environment. Markdown, Mermaid source, text trees, and relationship tables remain valid core outputs without installing a renderer, runtime, package manager, or online service.

The installable skill lives in [`skills/topology/`](skills/topology/). Everything else in this repository (README, license, validator, tests, CI) is repository tooling that hosts never install and the skill never reads.

## Install

Install commands were last verified on 2026-09-22 against the platform documentation linked below. Re-check a command if the host's CLI has released a new major version since then.

### Skills CLI (`npx skills`, any host)

Install for the agents detected in the current project:

```sh
npx skills add Sisyphe42/topology-skill --skill topology
```

Install globally for a specific agent, for example Codex:

```sh
npx skills add Sisyphe42/topology-skill --skill topology --agent codex --global
```

Use the skill once without installing it:

```sh
npx skills use Sisyphe42/topology-skill@topology
```

The Skills CLI copies into `.agents/skills/topology` (or `~/.agents/skills/topology` with `--global`) and symlinks into each detected agent directory. Use `--copy` when symlinks are unavailable or undesirable. Docs: https://skills.sh/docs.

### Claude Code

Copy `skills/topology/` into `~/.claude/skills/` (personal) or `<project>/.claude/skills/` (project), or install through the Skills CLI above, which symlinks into `.claude/skills/` automatically. Docs: https://code.claude.com/docs/en/skills.

### Codex / ChatGPT

Codex scans `.agents/skills/` from the working directory up to the repository root, and `~/.agents/skills/` for user scope. The Skills CLI command above writes there. Alternatively, use the bundled installer skill inside Codex:

```text
$skill-installer install https://github.com/Sisyphe42/topology-skill/tree/main/skills/topology
```

The optional `agents/openai.yaml` sidecar supplies the display name and default prompt in the Codex and ChatGPT UI. Docs: https://developers.openai.com/codex/skills.

### OpenSkills

```sh
npx openskills install Sisyphe42/topology-skill
```

Installs into `./.claude/skills/` by default; add `-g` for `~/.claude/skills/`. Docs: https://github.com/numman-ali/openskills.

### OpenClaw

```sh
openclaw skills install skills-sh:Sisyphe42/topology-skill/topology
```

Or `openclaw skills install git:Sisyphe42/topology-skill@main` for the whole repository. Docs: https://docs.openclaw.ai/tools/skills.

### Hermes Agent

```sh
hermes skills install skills-sh/Sisyphe42/topology-skill/topology
```

Or add the repository as a tap with `hermes skills tap add Sisyphe42/topology-skill`. Docs: https://hermes-agent.nousresearch.com/docs/user-guide/features/skills.

## What it does

- Inspects available evidence before asking questions.
- Chooses structural, dependency, flow, deployment, process, entity, or change topology based on the goal.
- Delivers small topologies directly in the conversation.
- Uses a concentrated decision gate before unresolved high-impact persistent writes.
- Keeps verified current state, inference, and proposed state distinct.
- Treats rendering, package installation, containers, browsers, and online platforms as optional capabilities.
- Maintains one source of truth and incrementally updates existing topology artifacts.

## Compatibility

The skill uses only the core Agent Skills frontmatter keys (`name`, `description`, `license`, `compatibility`), so it uploads unchanged to claude.ai and the Claude Skills API, and installs through any scanner that recognises the `skills/<name>/SKILL.md` layout (Skills CLI, OpenSkills, Claude plugin marketplaces, Hermes taps, ClawHub).

No npm package, build step, credentials, or environment variables are required. Optional rendering guidance is documented inside the skill and never authorizes automatic installation, upload, publication, or sharing.

## Repository layout

```text
skills/topology/                      Portable skill: the only thing hosts install
  SKILL.md                            Skill entry point
  agents/openai.yaml                  Optional Codex/ChatGPT UI metadata
  references/decision-standard.md     Decision and complexity rules
  references/format-routing.md        Format and delivery routing
  references/artifact-contract.md     Persistent and inline output contract
  references/rendering.md             Blank-environment rendering fallback
scripts/validate_skill.py             Dependency-free validator (repository tooling)
tests/behavior-cases.md               Prompt-level forward-evaluation cases
.github/workflows/validate.yml        Windows and Ubuntu compatibility checks
.gitignore                            Ignores .env, build output, editor noise
LICENSE                               MIT license
```

## Development validation

The validator uses only the Python standard library and locates the skill from its own path, so it can run from any working directory. Run the skill, repository, and release checks with Python 3.12 or another current Python 3:

```sh
python scripts/validate_skill.py --repository
```

Validate an installed copy anywhere:

```sh
python scripts/validate_skill.py ~/.agents/skills/topology
```

Add the pinned Skills CLI discovery, prompt-generation, and isolated copy-install checks when Node.js is available:

```sh
python scripts/validate_skill.py --repository --npx-smoke
```

The CLI smoke test sets `DISABLE_TELEMETRY=1` and `DO_NOT_TRACK=1`. The six [forward behavior cases](tests/behavior-cases.md) document agent-level invariants separately; the validator confirms their presence without pretending to execute an LLM.

## Telemetry

The skill itself does not collect telemetry. The external Skills CLI may collect anonymous usage data according to its own documentation. Set `DISABLE_TELEMETRY=1` when invoking the CLI if you prefer to disable it.

## License

Released under the [MIT License](LICENSE). Copyright (c) 2026 Sisyphe42.
