# Canonical graph, version 1

Use JSON. Required top-level fields: `schema_version: 1`, `title`, `question`, nonempty `nodes` and `sources`. `summary`, `language` (default en), `edges`, `groups`, `steps`, `scenarios`, `uncertainties` are optional. The supported `default_view` values are `map`, `focus` and `path` (default `map`). Optional `source_license` contains the exact repository license notice for embedded excerpts; it is preserved in HTML and SVG exports. Strings are data, never HTML.

```json
{
  "schema_version": 1,
  "title": "Delivery mechanism",
  "question": "How does a message get retried?",
  "nodes": [
    {"id":"queue", "label":"Outbox", "kind":"queue", "description":"Stores pending deliveries.", "source_ids":["queue-src"]},
    {"id":"worker", "label":"Delivery worker", "kind":"service", "description":"Claims and sends due items.", "source_ids":["worker-src"]}
  ],
  "edges": [
    {"id":"claim", "from":"worker", "to":"queue", "relation":"claims", "label":"claim due item", "source_ids":["worker-src"]},
    {"id":"retry", "from":"worker", "to":"queue", "relation":"retries", "label":"schedule failed attempt", "source_ids":["worker-src"]}
  ],
  "sources": [
    {"id":"queue-src", "path":"src/outbox.py", "start":20, "end":35},
    {"id":"worker-src", "path":"src/worker.py", "start":45, "end":70}
  ],
  "uncertainties": ["Illustrative schema example: replace names and ranges with actual inspected code."]
}
```

The example is a schema illustration, not a verified repository claim. IDs use ASCII letters, digits, underscore, dash and dot, beginning with a letter/digit. IDs within each collection are unique.

Nodes: `id`, `label`, `kind`, optional `description`, optional short `caption` (at most 180 characters), optional `group`, `source_ids`. Kinds: module, function, service, store, queue, actor, artifact, input, process, decision, output, external. Do not rely on shape to encode meaning; labels are primary.

Edges: `id`, `from`, `to`, meaningful `relation`, optional `label`, `source_ids`. Cycles, self-edges, multiple edges between the same endpoints and disconnected components are legal. No implied ordering.

Groups: `id`, `label`, optional `parent`. Node.group references a group. Nested groups form a tree/forest; group nesting cannot cycle. Group IDs must differ from node IDs.

Evidence: default `evidence: source` requires at least one source ID. Use `evidence: inferred`, `reason` and available source IDs for an unverified interpretation. Inferred edges are visibly differentiated. Do not mark runtime observations in this schema; it does not certify traces.

Sources: repository-relative POSIX `path`, 1-based inclusive `start`, `end`. Preparation captures SHA256 of exact bytes, excerpt and excerpt hash. If an existing fingerprint/excerpt/revision is supplied it must match. Never strip fingerprints to conceal drift: re-inspect and regenerate affected claims. An exact clean Git blob may get a pinned GitHub URL. No absolute local path or authenticated origin is embedded.

Optional steps: `id`, `title`, `description`, `node_ids` nonempty, `edge_ids`, `source_ids`, `duration_ms` (100–60000, default 2400), evidence. These are highlights over the same graph; they never determine its topology. Scenarios: `id`, `label`, nonempty `step_ids`. Without steps the player provides a clearly labeled component tour, not an execution sequence.

Unknowns: use `uncertainties` for omitted dynamic behavior, unresolved dependencies and limits of inspection. A valid file means structurally valid and matching source bytes, not semantically proven.

## Compact introduction

Keep `summary` concise. The explorer formats component/relationship counts, current walkthrough duration and a short revision separately. A long summary remains available in a disclosure instead of occupying the first viewport.

Optional `overview` supports a short `lead` and a `path` of existing component references, for example `{"lead":"A local property appraisal tool.","path":[{"node_id":"ui","label":"React"},{"node_id":"api","label":"FastAPI"}]}`. Every `node_id` must exist. Labels are plain display text; topology and source evidence stay in the original graph. This orientation row does not imply direct calls or recorded execution.

## Diagram presentation

Optional `presentation` affects layout only:

```json
{"presentation":{"layout":"flow","top":["provider"],"bottom":["state"]}}
```

`layout` is `auto` (default), `layered` or `flow`. Auto uses horizontal flow only for a small, ungrouped acyclic chain when the available graph width keeps labels readable; otherwise it retains layered routing. Expanding the diagram exposes more room; if a complete-map fit would make text too small, it starts at a readable selected detail with pan and an explicit Fit overview. Grouped and dense graphs retain their topology and established automatic layout.

Explicit flow supports 1–8 main components and optional `top`/`bottom` lists of up to two existing node IDs each. Shared bands are actual sourced components, not invented buses or duplicate nodes. A component can appear in only one band. Flow bands cannot be combined with groups or `layout: layered`; scope a focused graph instead. Wide screens use a horizontal main flow; below 800px it becomes vertical without changing components or relationships. The main graph still routes branches, cycles, parallel relationships and self-edges. Band relationships keep their canonical IDs, evidence and selectable source detail.

Prefer concise authored node captions that state responsibility, such as `"caption":"Claims due jobs and records the outcome"`. They render beneath the title, with measured wrapping and an explicit ellipsis when needed. Without a caption, the player displays a clipped description or kind; the inspector and tooltip retain the complete text. Captions have the same evidence obligations as other node display text. They never establish a relationship or execution order.
