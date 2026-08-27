# Topology Decision Standard

Use this reference to form the internal Topology Decision Packet. The packet guides behavior; do not dump it into the response unless the user asks for it.

## Decision dimensions

| Dimension | Autonomous default | Ask only when |
| --- | --- | --- |
| Goal and audience | Infer whether the job is structural, dependency, data-flow, runtime-flow, deployment, process, entity-relationship, or change topology, and whether the audience is technical, review, management, presentation, or public. | Multiple plausible interpretations would materially change the abstraction or disclosure. |
| Scope and state | Include only entities relevant to the question. Identify exclusions. Keep verified current state, user-stated state, inferred state, and proposed state distinct. | The boundary changes the main conclusion, or current and target state cannot be separated reliably. |
| Viewpoint | Give each view one main question. Use an overview plus details when concerns differ. | Choosing one viewpoint would exclude another equally important requested outcome. |
| Format | Prefer Markdown with embedded Mermaid when it is renderable and sufficient. Route by the format guide. | A choice introduces an unavailable tool, substantial maintenance, external action, or irreversible conversion. |
| Delivery and location | Prefer Inline for a Focused disposable result. For durable output, follow existing conventions; otherwise use `docs/topology.md` in software repositories or `topology.md` for general goals. | The write affects an existing source of truth, public location, external system, or unresolved convention. |
| Source of truth | Incrementally maintain the existing authoritative artifact. Use one primary entry point. | Existing artifacts conflict or ownership cannot be established. |
| Complexity | Classify relevant abstract components rather than raw files. Apply the limits below. | A different class changes the expected number of deliverables or substantially affects comprehension. |
| Semantics | Infer stable domain names, typed relationships, direction, grouping, states, and a minimal legend. | Domain semantics remain ambiguous after source inspection. |
| Evidence | Trace current claims to files, configuration, command output, supplied material, or explicit user statements. Mark inference and confidence. | Sources conflict, are inaccessible, or do not support a confident current-state claim. |
| Sensitivity | Abstract secrets, personal data, internal addresses, and unnecessary security details. | The requested disclosure is public, sensitive, or broader than needed for the topology. |
| Lifecycle | For durable output, record verification date and what changes should trigger an update. | The user needs ownership, publication workflow, scheduled maintenance, or compliance metadata. |
| External actions | Prefer local output. | Any Figma, online, sharing, publishing, or remote overwrite action is proposed; it needs explicit authorization. |

## Asking policy

Inspect first. Explicit user choices count as confirmed. Decide low-impact matters without asking, including layout direction, exact Mermaid diagram family, ordinary naming normalization, legend placement, and how to split a view within the limits below.

Before the first persistent write, collect only unresolved high-impact decisions into one gate. Do not ask separate questions over multiple turns when they can be decided together. Do not ask for information the environment already answers.

Inline output does not need a gate. If an Inline result exposes a genuine ambiguity, state the selected interpretation as an assumption and proceed when the alternative would not create material risk.

Explicit authorization for a local artifact does not authorize an external artifact. Authorization to create an external artifact does not authorize publishing, sharing, or overwriting a different remote artifact.

## Complexity classes

Count relevant abstract components, not files, functions, or every discovered resource.

### Focused

- One main question.
- At most 12 nodes and 18 edges.
- One primary view.
- At most two grouping levels.
- Default delivery: Inline, unless the user asks for a file or durable maintenance is clearly required.

### Standard

- An overview plus one to three detail views.
- At most 20 nodes and 30 edges per view.
- At most three grouping levels per view.
- Default delivery: persistent local artifact, unless the user explicitly wants only an immediate conversation result.

Use Standard when a single view would hide a meaningful layer or flow even if the raw node count remains small.

### Complex

Use Complex when the relevant scope has more than 25 nodes, more than three domains, more than two independent kinds of flow, or another cross-cutting concern that cannot remain readable in Standard small multiples.

- Start with a stable overview.
- Add focused views organized by domain, lifecycle, flow, or another evidenced boundary.
- Keep every individual view within the Standard per-view limits.
- Do not create one comprehensive hairball diagram.

## State and evidence labels

Use the smallest label set that remains honest:

- `verified-current`: confirmed from an accessible source in this run.
- `user-stated`: supplied by the user but not independently verified.
- `inferred`: supported indirectly and explicitly identified as inference.
- `proposed`: target state or recommendation that does not yet exist.
- `unknown`: material relationship that cannot be established.

Do not imply that `proposed` or `inferred` is deployed, implemented, validated, or current.

## Optional suggestions

After delivering the topology, mention an autonomous choice only when knowing it helps the user make a later decision. Use at most three suggestions, label them non-blocking, and state the consequence rather than asking for retrospective approval.

Useful example pattern: “Current view follows runtime dependencies; a domain-level companion view may be more suitable for management review.”

Do not include suggestions when they merely restate the result, advertise another format, or create work unrelated to the request.

