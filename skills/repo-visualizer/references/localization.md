# Language and appearance

Output language follows the user's explicit request, then their conversation language. It is independent of the agent vendor and the repository's programming or documentation language.

Set `language` to a BCP-47 tag such as `en`, `cs`, `de` or `fr`. Write labels, title, question, descriptions, scenarios, steps and uncertainties in that language. Keep code excerpts, paths, identifiers and license notices unchanged.

English, Czech, German, French and Spanish interface catalogs are bundled. For another language, read `assets/locales/en.json` and translate every value into the graph's `ui_strings` object. Keep keys and placeholders such as `{nodes}`, `{edges}`, `{format}` and `{percent}` unchanged. Values are plain text, never translated HTML.

The language menu shows native names and flag icons. It switches the interface and changes graph content only when a graph translation was supplied. A notice explains when the graph remains in its original language. A standalone graph defaults to its declared language; the public site can use the browser preference. Sun, moon and monitor buttons select light, dark and system appearance. Choices persist locally when storage is available, and still work when it is blocked.

For a bilingual graph, `translations` is an optional object keyed by language tag:

```json
{
  "translations": {
    "cs": {
      "question": "Co se stane při minutí cache?",
      "nodes": {"cache": {"label": "Cache", "description": "Vrátí uložený výsledek."}},
      "edges": {"miss": {"label": "výsledek chybí"}},
      "groups": {"backend": {"label": "Backend"}},
      "steps": {"lookup": {"title": "Vyhledat výsledek", "description": "Nejdříve ověří cache."}},
      "scenarios": {"request": {"label": "Požadavek"}}
    }
  }
}
```

Translations are display-only. They cannot change topology, ids, sources or fingerprints. Nodes allow `label` and `description`; edges, groups and scenarios allow `label`; steps allow `title` and `description`. Omitted values retain the original text. Supply all relevant fields for a complete graph translation.

Local deterministic exports accept `--theme light|dark|system` and `--language <tag>`. Interface language, graph translation and original code evidence are separate. A language switch never rewrites source excerpts.
