# Language and appearance

Every new explanation includes English (`en`), Czech (`cs`), German (`de`), French (`fr`) and Spanish (`es`). This is independent of the agent vendor and the repository's programming or documentation language. The user's explicit language request, then their conversation language, chooses the initial view; it does not reduce the set of translated explanations.

Set `language` to the primary BCP-47 tag and author the canonical title, question, summary, components and walkthrough in that language. Supply the other four languages in `translations`. If the primary language is outside the five bundled languages, supply all five in addition to it. Keep source excerpts, paths, actual code symbols, IDs, fingerprints and exact license notices unchanged. Proper names such as Codex, Whisper and Redis may remain the same.

## Complete explanation coverage

For each translation, include all populated explanation fields:

- `title`, `question` and `summary`.
- Every node's `label`, `description`, `caption` and inference `reason`, when present.
- Every edge's `label`, displayed `relation` and inference `reason`, when present.
- Every group and scenario `label`.
- Every step's `title`, `description` and inference `reason`, when present.
- Every `uncertainties` entry, retaining the same scope and caveats.
- `overview.lead` and every `overview.path` label, preserving component IDs and order.

Translations are display-only. They cannot replace sources, evidence status, endpoints, topology or presentation settings. Translating a relationship's display text does not change the canonical relationship. Captions remain within 180 characters. Translate prose around code symbols while retaining the symbols verbatim. Do not replace factual caveats with promotional text or invent missing semantics.

This abbreviated example shows the shape, not a complete five-language artifact:

```json
{
  "translations": {
    "cs": {
      "title": "Vyhledání v cache",
      "question": "Co se stane při minutí cache?",
      "summary": "Cache vrátí výsledek, nebo předá požadavek pracovníku.",
      "overview": {
        "lead": "Vyhledání a předání požadavku.",
        "path": [{"node_id":"cache","label":"Cache"}]
      },
      "nodes": {"cache": {"label":"Cache","description":"Vrátí uložený výsledek.","caption":"Uchovává dostupné odpovědi"}},
      "edges": {"miss": {"label":"výsledek chybí","relation":"předává"}},
      "groups": {"backend": {"label":"Backend"}},
      "steps": {"lookup": {"title":"Vyhledat výsledek","description":"Nejdříve ověří cache."}},
      "scenarios": {"request": {"label":"Požadavek"}},
      "uncertainties": ["Statická analýza zdrojů, nikoli záznam skutečného běhu."]
    }
  }
}
```

Use `--all-languages` for prepare, validate and build:

```sh
python3 <skill>/scripts/repo_story.py prepare graph.json --repo <repo> --all-languages --ordered -o prepared.json
python3 <skill>/scripts/repo_story.py build prepared.json --all-languages --ordered -o explorer.html
```

Missing fields produce an error naming the languages and field paths, before an output is written. Fill the translations and rerun. This verifies coverage, not linguistic accuracy; read the translated explanations and check that caveats retain their meaning. The lower-level format still accepts older partial/single-language artifacts without the flag; that compatibility is not the default workflow for new skill output. Omitted fields in those older files retain their original text.

## Interface and exports

All five interface catalogs are bundled. For an additional requested language, translate every value from `assets/locales/en.json` into the graph's `ui_strings` object. Keep keys and placeholders such as `{nodes}`, `{edges}`, `{format}` and `{percent}` unchanged. Values are plain text, never translated HTML.

The language menu switches the interface and the supplied graph explanation. Verify all five choices in the actual HTML, including a selected relationship, a walkthrough step and the limitations disclosure. A standalone graph defaults to its primary language; the public site defaults to English. Appearance and language choices persist locally when storage is available and work when it is blocked.

Deterministic exports accept `--theme light|dark|system` and `--language <tag>`. A GIF/video uses the selected export language; the HTML and canonical JSON keep all supplied languages, regardless of the current interface selection. Export additional language variants when requested. A language switch never rewrites source excerpts.
