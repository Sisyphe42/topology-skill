# Topology Artifact Contract

Apply the full contract to persistent local or external topology work. Inline output uses the smaller contract below.

## Persistent Markdown companion

Use one Markdown entry point that contains or links the authoritative visual source. Adapt headings to an established repository convention, but preserve the following information:

1. **Purpose and status** — the question answered, intended audience, and whether the content is current, proposed, or a comparison.
2. **Scope and exclusions** — included boundary plus material omissions.
3. **Decision record** — primary format, delivery location, viewpoint, complexity class, and source-of-truth choice. Include only decisions useful to future maintainers.
4. **Legend and semantics** — node kinds, edge kinds, direction, grouping, and state styling when they are not self-evident.
5. **Topology views** — a readable overview and only the focused views required by the complexity class.
6. **Evidence and confidence** — sources for current-state claims and labels for user-stated, inferred, proposed, or unknown content.
7. **Target deltas** — when a target state exists, describe the changes without implying implementation.
8. **Open questions** — only unresolved facts that materially affect the topology.
9. **Lifecycle** — last verified date and concrete changes that should trigger revalidation.
10. **Visual reference** — for a separate local or authorized external artifact, record its path or stable reference.

Do not include empty ceremonial sections. If a required concept does not apply, represent it compactly in the purpose or decision record rather than adding boilerplate.

## Inline contract

An Inline response needs only:

- a short scope statement;
- a state label such as current, proposed, or current-to-target;
- the rendered topology;
- a minimal legend when an edge, style, or status is not obvious;
- a material assumption or uncertainty, if one exists.

Do not surround a small Inline result with a full report. Do not create a file in addition to the response unless the user explicitly asked for one.

## View construction

- Give each view a descriptive title that states its question or boundary.
- Use stable, domain-relevant node names rather than file paths when the node represents a subsystem or concept.
- Type edges when multiple relationship kinds appear, such as `calls`, `reads`, `publishes`, `depends on`, `contains`, or `hands off to`.
- Make direction explicit. For bidirectional relationships, show two directed edges or define a bidirectional edge in the legend.
- Use grouping for evidenced boundaries, not decorative boxes.
- Preserve identifiers already used by an authoritative artifact unless they are wrong or misleading.
- Separate current and proposed views when styling alone would not prevent confusion.

## Incremental update rules

Before changing an existing artifact:

1. Identify whether it is authoritative, generated, embedded, or an export.
2. Inspect references and callers before renaming, moving, or replacing it.
3. Preserve valid scope choices, identifiers, links, terminology, and explicit human decisions.
4. Update verified facts and mark anything that can no longer be verified.
5. Keep corrections to prose and metadata consistent with the actual visual source.
6. Do not edit only an export when an editable source exists.
7. If multiple artifacts claim authority, stop before writing and present one concentrated reconciliation decision.

## Validation

Validate what the selected format makes observable:

- local paths and links resolve;
- diagram syntax parses or renders when a renderer is available;
- companion metadata points to the correct visual artifact;
- node and edge counts respect the chosen complexity class;
- no secret or unnecessary sensitive identifier appears;
- current, inferred, user-stated, unknown, and proposed content cannot be confused;
- the update leaves one clear source of truth.

