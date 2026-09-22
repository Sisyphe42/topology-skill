# Rendering in an Unknown Environment

Use this reference only when rendering capability affects the requested result. The skill must remain functional in a blank environment.

## Baseline contract

Markdown, Mermaid source, a text tree, or a relationship table is the portable baseline. Do not make Node.js, Python, Java, a browser, a package manager, a container runtime, a diagram CLI, network access, or an online account mandatory for topology creation.

An unrendered but valid Mermaid block is a complete deliverable when the user asked for a topology, explanation, or source artifact. It is not a complete deliverable when the user explicitly requested SVG, PNG, PDF, a presentation-ready image, or proof that the diagram renders.

## Capability ladder

Use the first sufficient level. Do not climb the ladder merely to produce more files.

1. **Conversation or document-native rendering** — emit Mermaid directly when the current surface is known to render it.
2. **Existing local renderer** — use an already installed compatible tool such as `mmdc`, `dot`, or PlantUML when it matches the chosen source format.
3. **Authorized optional installation** — suggest or perform an install only when rendering is required, no sufficient renderer exists, and the user authorized the installation and its scope.
4. **Authorized container rendering** — use an existing Docker or Podman runtime only when container use is acceptable and the image source is trusted.
5. **Browser-assisted preview** — use a local page or manual editor only when a browser and any required network access are available. Disclose whether a CDN or remote service is involved.
6. **Source-only fallback** — preserve the topology source and explain what could not be rendered.

Do not assume that a command exists because a language manifest, operating system, or package manager is present. Probe the exact capability with a read-only command or metadata check when possible.

## Installation boundary

Installation changes the environment and may change a project manifest or lockfile. It is not implied by a request to create a topology. Before installing, state:

- the package or image and why it is needed;
- whether the install is project-local, user-global, system-global, or container-only;
- which files or environment state it will change;
- the expected output format;
- the source-only fallback if installation is declined or fails.

Use the package manager already selected by the project or user. Do not encode a personal filesystem path or one operating system's package-manager preference into the skill.

Stop after one failed installation attempt unless the error provides a clear, safe correction that stays within the same authorization. Never switch package manager, install scope, or online service silently.

## Mermaid routes

Prefer Mermaid for the portable default because its source remains human-readable and versionable without a renderer.

When Node.js and npm are already available and the user authorizes installation, Mermaid CLI can be installed project-locally:

```sh
npm install --save-dev @mermaid-js/mermaid-cli
```

Use a global install only when the user explicitly prefers a user- or system-wide CLI:

```sh
npm install --global @mermaid-js/mermaid-cli
```

After installation, discover the actual executable rather than assuming a platform-specific path. A typical render is:

```sh
mmdc -i topology.mmd -o topology.svg
```

For reproducible project-local installation, preserve the project's normal lockfile behavior and record the selected package version there. Do not add a package manifest to a non-Node project solely for optional topology rendering unless the user approves that tradeoff.

If Docker or Podman already exists, the official Mermaid CLI container is an alternative to host installation. Pin an image version for reproducible work, mount only the required working directory, and do not assume container execution is cheaper or permitted.

Official references:

- Mermaid CLI: <https://github.com/mermaid-js/mermaid-cli>
- Mermaid documentation: <https://mermaid.js.org/>

## Other local renderers

Use Graphviz only for DOT sources and PlantUML only for PlantUML/C4 sources. Do not install them to render Mermaid. Prefer their official distributions or the package manager already trusted by the target project. Keep the editable textual source beside any generated image.

Official references:

- Graphviz downloads: <https://graphviz.org/download/>
- PlantUML installation: <https://plantuml.com/starting>

## Browser and online routes

A static preview page that downloads Mermaid from a CDN is not offline or self-contained. Treat it as network-assisted local rendering, disclose the dependency, pin the library version when reproducibility matters, and do not add such a page unless it provides value beyond the Markdown source.

Mermaid Live Editor may be offered as a manual, zero-install preview option: <https://mermaid.live/>. Do not automatically upload, paste, publish, shorten, or share the topology. Warn that external export, Kroki, sharing, analytics, URL synchronization, or account-backed features may expose diagram content beyond the local workspace.

Do not use a public rendering API for private, security-sensitive, proprietary, or unknown-sensitivity topology. Self-hosted services still require explicit authorization and endpoint verification.

## Failure semantics

- If rendering was optional, return the inspectable source without treating missing tooling as task failure.
- If rendered media was required, report the missing capability and the smallest authorized next step.
- Preserve source files after a renderer failure.
- Do not present a stale export as the result of the current source.
- Do not claim success until the requested output file exists and can be inspected or its renderer reports a verified result.

## Compatibility checks

Exercise these scenarios when changing rendering guidance:

- no runtime, package manager, renderer, browser, or network;
- native Mermaid rendering is available;
- a compatible local CLI is already installed;
- installation is declined or forbidden;
- installation fails once;
- the environment is offline;
- the topology is sensitive and online rendering is unsafe;
- rendered media is explicitly required and must be inspected.
