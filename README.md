# topology-skill

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
```

## Telemetry

The skill itself does not collect telemetry. The external Skills CLI may collect anonymous usage data according to its own documentation. Set `DISABLE_TELEMETRY=1` when invoking the CLI if you prefer to disable it.

