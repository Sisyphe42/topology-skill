---
name: topology-skill
description: Analyze a directory or goal, decide an appropriate topology, and deliver it inline or as an approved persistent artifact. Use for structural, dependency, flow, deployment, process, or entity-relationship topology work; not for merely restyling an already-defined diagram.
---

# Topology Architecture

Build the smallest topology that answers the user's actual question. Inspect before asking, distinguish facts from proposals, and do not use topology work as permission to modify the system being described.

Assume a blank environment: no runtime, package manager, diagram CLI, browser automation, network access, or native diagram renderer is guaranteed. The core deliverable must remain useful as inspectable Markdown, Mermaid source, a text tree, or a relationship table without installing anything. Rendering is a capability enhancement, not a prerequisite for topology work.

## Start With Read-Only Discovery

Read the full request, then inspect the current directory and relevant existing sources before choosing a topology. Look for existing architecture or topology artifacts, repository guidance, manifests, entry points, dependency declarations, deployment configuration, and terminology that should be preserved.

For a non-software goal, inspect whatever sources the user supplied and identify the entities, relationships, flows, states, and boundary implied by that goal. Do not force a software-architecture model onto a general process or relationship problem.

Do not ask for facts that can be discovered safely. Do not treat inaccessible or inferred information as verified current state.

## Decide Before Delivering

Form an internal Topology Decision Packet covering goal, audience, scope, state, viewpoint, format, delivery mode, location, source of truth, complexity, semantics, evidence, sensitivity, lifecycle, and external actions.

Read [references/decision-standard.md](references/decision-standard.md) when choosing these decisions or deciding whether user input is required.

- Treat explicit choices in the request as confirmed.
- Decide low-impact details autonomously.
- If a persistent artifact still has unresolved high-impact choices, ask about all of them in one concentrated gate before the first write.
- Do not ask merely to confirm an obvious default.
- Inline output requires no write gate because it does not mutate a file or external system.
- External publication, sharing, remote overwrite, or creation in Figma or another online tool always requires explicit authorization for that external action.

## Choose a Delivery Mode

Read [references/format-routing.md](references/format-routing.md) when selecting a format, location, renderer, or external destination. Read [references/rendering.md](references/rendering.md) when the user requires a rendered file, native rendering is uncertain, or installation, a container, a browser preview, or an online service is being considered.

### Inline

Use Inline when the user requests an in-conversation result, or when the result is Focused, has one view, and does not need durable collaboration or maintenance. Render the result directly as concise Markdown, a table, a text tree, or Mermaid. Do not also create a file unless the user asked for one.

If the conversation surface does not render Mermaid, show the fenced Mermaid source. This is still a complete Inline topology unless the user explicitly required a rendered image or document.

State the scope, whether the topology is current or proposed, and any material assumption near the diagram. A full document wrapper is unnecessary.

### Local artifact

Use a local artifact when the user requests a file or the topology needs maintenance, citation, multiple views, or version control. Respect an existing documentation convention and source of truth. Otherwise use `docs/topology.md` for a software repository and `topology.md` in the current directory for a general goal.

Before editing an existing artifact, inspect its callers, identifiers, links, status vocabulary, and factual basis. Update it incrementally. Preserve valid user decisions and stable identifiers; do not silently overwrite, fork a competing source of truth, or convert an inference into a fact.

### External artifact

Use Figma, an online whiteboard, or another external destination only when it materially improves the requested outcome, the required tool is available, and the user has authorized the external write. If the tool is unavailable, say so and offer a local format that preserves the intended structure. Never claim an external artifact was created without a confirmed result.

### Hybrid

For a complex persistent result, give a small in-conversation overview and link the local or authorized external artifact. Keep the overview consistent with the durable source.

## Build the Topology

Each view should answer one main question. Keep current facts and proposed states visually and textually distinct. Define non-obvious node and edge semantics, direction, grouping, and status. Split dense graphs into an overview and focused views rather than shrinking or crowding one diagram.

For persistent output, read and follow [references/artifact-contract.md](references/artifact-contract.md). Non-Markdown visual artifacts require a Markdown companion manifest; the visual alone is not sufficient for scope, evidence, assumptions, and lifecycle.

Do not expose secrets, personal data, internal addresses, or unnecessary security-sensitive details. Redact or abstract them while preserving the relationship needed by the topology.

## Finish and Verify

Check that:

- the chosen mode and format match the task and available environment;
- the result remains inspectable when no renderer or network is available;
- every current-state claim has a discoverable source or is labelled with its confidence;
- proposed nodes and edges are marked `proposed` and cannot be mistaken for current state;
- the view limits and split rules in the decision standard are respected;
- referenced files, identifiers, links, and diagram syntax are valid where they can be checked;
- an incremental update did not create a second source of truth.

When rendered media was explicitly required, verify the actual rendered file. When it was not required, do not install software or introduce a rendered derivative merely to make the result appear more complete.

After delivery, add an optional suggestions section only when an autonomous decision has a meaningful consequence for maintenance, accuracy, extensibility, or presentation. Give at most three concise, non-blocking suggestions. Explain the consequence of the chosen default; do not repeat the decision packet, invent busywork, or expand the task. Omit the section when there is no useful suggestion.
