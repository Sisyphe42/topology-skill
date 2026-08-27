# topology-skill

[![Validate](https://github.com/Sisyphe42/topology-skill/actions/workflows/validate.yml/badge.svg)](https://github.com/Sisyphe42/topology-skill/actions/workflows/validate.yml)
[![Release](https://img.shields.io/github/v/release/Sisyphe42/topology-skill)](https://github.com/Sisyphe42/topology-skill/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A portable Agent Skill for inspecting a directory or goal, deciding the right topology, and delivering it inline or as an approved persistent artifact.

The skill assumes a blank environment. Markdown, Mermaid source, text trees, and relationship tables remain valid core outputs without installing a renderer, runtime, package manager, or online service.

## Install with `npx skills`

Install for the agents detected in the current project:

```sh
npx skills add Sisyphe42/topology-skill --skill topology-skill
```

Install globally for Codex:

```sh
npx skills add Sisyphe42/topology-skill --skill topology-skill --agent codex --global
```

Use the skill once without installing it:

```sh
npx skills use Sisyphe42/topology-skill@topology-skill
```

List the skill before installation:

```sh
npx skills add Sisyphe42/topology-skill --list
```

The Skills CLI installs Codex project skills under `.agents/skills/` and global Codex skills under `~/.codex/skills/`. Use `--copy` when symlinks are unavailable or undesirable.

## What it does

- Inspects available evidence before asking questions.
- Chooses structural, dependency, flow, deployment, process, entity, or change topology based on the goal.
- Delivers small topologies directly in the conversation.
- Uses a concentrated decision gate before unresolved high-impact persistent writes.
- Keeps verified current state, inference, and proposed state distinct.
- Treats rendering, package installation, containers, browsers, and online platforms as optional capabilities.
- Maintains one source of truth and incrementally updates existing topology artifacts.

## Compatibility

The repository uses the standard root-level `SKILL.md` layout recognized by the open Skills CLI. The required skill metadata is limited to `name` and `description`; Codex-specific interface metadata in `agents/openai.yaml` is optional and does not replace the portable skill entry point.

No npm package or build step is required to install or use the skill. Optional rendering guidance is documented inside the skill and never authorizes automatic installation, upload, publication, or sharing.

## Repository layout

```text
SKILL.md                         Portable skill entry point
agents/openai.yaml               Optional Codex UI metadata
references/decision-standard.md  Decision and complexity rules
references/format-routing.md     Format and delivery routing
references/artifact-contract.md  Persistent and inline output contract
references/rendering.md          Blank-environment rendering fallback
scripts/validate_skill.py        Dependency-free repository validator
tests/behavior-cases.md           Prompt-level forward-evaluation cases
.github/workflows/validate.yml   Windows and Ubuntu compatibility checks
LICENSE                          MIT license
```

## Development validation

The validator uses only the Python standard library. Run the structural and release checks with Python 3.12 or another current Python 3 version:

```sh
python scripts/validate_skill.py . --repository
```

Add the pinned Skills CLI discovery, prompt-generation, and isolated copy-install checks when Node.js is available:

```sh
python scripts/validate_skill.py . --repository --npx-smoke
```

The CLI smoke test sets `DISABLE_TELEMETRY=1` and `DO_NOT_TRACK=1`. The six [forward behavior cases](tests/behavior-cases.md) document agent-level invariants separately; the validator confirms their presence without pretending to execute an LLM.

## Telemetry

The skill itself does not collect telemetry. The external Skills CLI may collect anonymous usage data according to its own documentation. Set `DISABLE_TELEMETRY=1` when invoking the CLI if you prefer to disable it.

## License

Released under the [MIT License](LICENSE). Copyright (c) 2026 Sisyphe42.
