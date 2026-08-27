# Format and Delivery Routing

Choose one primary source of truth. Do not generate equivalent formats merely because tools are available.

## Routing matrix

| Format | Prefer when | Avoid when | Persistence rule |
| --- | --- | --- | --- |
| Markdown prose, table, or text tree | The relation set is very small, textual precision matters, or the result is an immediate explanation. | Direction, cycles, branching, or grouping would be harder to understand in text. | May be Inline or the Markdown source of truth. |
| Mermaid | A versionable structure, dependency, flow, sequence, state, or relationship diagram is sufficient. Mermaid source remains useful even when the current surface cannot render it. | Required layout control is unavailable or the graph is too dense for a readable view. | Default: embed in the Markdown source of truth. |
| Graphviz | Dense directed graphs need deterministic automatic layout and the environment already supports rendering. | The user needs easy manual editing or the toolchain is absent. | Keep the textual source and link generated exports; do not make a binary export the only source. |
| PlantUML or C4 | Formal software boundaries and an existing compatible toolchain make the notation useful. | The notation would be introduced solely for this task or the audience does not understand it. | Keep the textual source and its Markdown companion. |
| Excalidraw | Free spatial composition, workshop annotation, or hand-drawn communication is the primary value. | Precise source diffs, automatic regeneration, or dense formal semantics dominate. | Save the local source plus a Markdown companion manifest. |
| Figma | Presentation polish, deliberate composition, and an available Figma connection materially improve the requested outcome. | A local versionable format is sufficient, the connector is unavailable, or no external write was authorized. | Maintain a Markdown companion with the file/node reference and evidence boundary. |
| Other online platform | Real-time collaboration or publication is explicitly required. | The same outcome is possible locally or external authorization is absent. | Record the authorized destination in a local Markdown companion when a local workspace exists. |

## Delivery choice

Choose `Inline` when the output is Focused and disposable, or when the user explicitly asks to see it in the conversation. Render it directly. A request to explain, sketch, show, or compare a small topology normally implies Inline, not file creation.

Choose `Local artifact` when the user requests a file, an existing topology must be maintained, the result has multiple views, or it needs version control, citation, or future updates.

Choose `External artifact` only with explicit authorization and a confirmed available tool. Tool availability is not authorization. A desired format is not proof that the external write succeeded.

Choose `Hybrid` for a complex persistent result: show a small overview in the response and link the durable artifact. Do not paste every detailed view into the conversation.

## Location choice

For a persistent artifact:

1. Preserve an existing authoritative location and naming convention.
2. Otherwise follow repository documentation guidance or nearby architecture-document conventions.
3. Otherwise use `docs/topology.md` for software repositories.
4. For a general goal without a repository convention, use `topology.md` in the current directory.

Associated visual sources should live beside the Markdown companion and use the same basename where practical, such as `topology.excalidraw` with `topology.md`.

Do not write into a README, specification, or product document merely because it exists. Embedding is appropriate only when that file is already the authoritative home for the described architecture and the user has authorized its modification.

## Render and fallback behavior

- Begin from a blank-environment assumption and discover capabilities rather than inferring them from the operating system or current machine.
- Verify that the selected syntax can be rendered by the available environment when practical.
- If Mermaid rendering is unavailable, its fenced source remains an acceptable local, inspectable deliverable when the user did not require a rendered image.
- If a requested specialized tool is unavailable, preserve the topology semantics in the closest local textual format and explain the limitation.
- Do not replace an explicitly requested editable source with only PNG, SVG, PDF, or a screenshot.
- Do not upload, publish, share, or create a remote document as an unannounced fallback.
- Do not install a runtime, package, browser, extension, or diagram engine merely because rendering is possible. Follow the capability ladder and authorization rules in [rendering.md](rendering.md).

