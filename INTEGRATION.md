# Data-layer integration note — swapping static JSON for the D1 API

The site is fully static today: `tools/build_data.py` generates `data/*.json`
from the frozen datasets, and every page reads them through one funnel.
When the Cloudflare D1 layer (decided 2026-11-07; `api.` subdomain) goes
live, **no page code changes** — only the funnel moves.

## The swap point

`assets/app.js`:

```js
GC.resolveData = function (name) { return 'data/' + name; };
GC.load = function (name) { return fetch(GC.resolveData(name)).then(r => r.json()); };
GC.api = { items(), stats(), questions(), discordant(), compare(),
           dynamics(), zombies(), pmidIndex(), citations(), coverage(),
           verification(), downloads() }  // all thin wrappers over GC.load
```

To cut over, change `GC.resolveData` to map each file to its API endpoint,
e.g. `return 'https://api.guide.erbihou.org/v1/' + name.replace(/\.json$/, '')`,
optionally with a static-file fallback on fetch failure. Pages call only
`GC.load(...)` / `GC.api.*()`, so signatures and payload shapes stay identical.

## Endpoint ↔ payload map (shapes are the contract)

| Static file | API endpoint (proposed) | Shape |
|---|---|---|
| `items.json` | `GET /v1/items` (+ `?doc=&tier=&str=&dir=&piv=&topic=&q=`) | array of recommendation records (805) |
| `stats.json` | `GET /v1/stats` | object: corpus / l1…l5 headline blocks |
| `pmid_index.json` | `GET /v1/pmid/:pmid` (single-record lookup) | map pmid → {title, cites[], pivotal_for[]} |
| `citations.json` | `GET /v1/citations?q=&year=&design=&pivotal=1` | array of {pmid, title, author, year, journal, design, cites[], pivotal_for[], n_cites, n_pivotal} |
| `pmid_coverage.json` | `GET /v1/coverage` | object: attachment/resolution counts + forward-index field coverage + `resolution_source` |
| `questions.json` | `GET /v1/questions` (+ `?q=`) | array of union questions with members |
| `discordant.json` | `GET /v1/discordant` | array of discordant pairs (a/b sides) |
| `compare.json` | `GET /v1/compare?a=&b=` | array of {a, b, name_a, name_b, pairs, both_stanced, concordant, discordant} per document pair |
| `dynamics.json` | `GET /v1/dynamics` | array of L5 transitions |
| `zombies.json` | `GET /v1/zombies` | object: zombie strata + notices |
| `verification.json` | `GET /v1/verification` | object: audit rounds, error rates |
| `downloads.json` | `GET /v1/downloads` | array of frozen-file entries |

Server-side filtering for `items` / `citations` is optional: both payloads are
small enough to ship whole and filter client-side, exactly as today. If the
API filters server-side, keep the response shapes identical and the pages
will not notice.

## Loading D1

`tools/build_data.py` stays the single ETL: the JSON files it emits are the
seed payloads. A D1 loader should consume the same files (one table per
payload, or a `payloads(name, json)` table for the object-shaped ones) so the
frozen-data discipline — every number generated from the frozen datasets,
assertions in the build — carries over unchanged. After loading, re-point
`GC.resolveData`, redeploy the static shell, and the static layer remains the
fallback: every page must keep working if the API is unreachable (serve the
last generated `data/*.json` alongside).

## v2 additions

The v1 worker (`worker/guide-api-mini.js`, live) serves `/v1/health`,
`/v1/stats`, `/v1/by-pmid`, `/v1/citation-search`, `/v1/item` and
`/v1/question` from the D1 tables `items / questions / citations / links`,
seeded from this site's own `data/*.json` via the internal seed route.
`worker/guide-api-v2.js` is a drop-in replacement (same routes, same seed
behaviour, same CORS) that adds four read endpoints:

| Endpoint | Returns |
|---|---|
| `GET /v1/guidelines` | `[{doc, guideline, society, year, n_items}]` for the 31 documents, sorted by `doc` |
| `GET /v1/search?q=` | `{q, items[≤40], citations[≤40], questions[≤40]}` — items match on `rec = q` or a `LIKE` over the record JSON; citations on `pmid = q` or title/author/journal `LIKE`; questions on a `LIKE` over the question JSON. Empty `q` returns three empty lists. |
| `GET /v1/citation?pmid=` | `{citation, citing: [{rec, doc, guideline, year, direction, tier, pivotal}], counts: {cites, pivotal, docs}}` — `links ⋈ items` for the citing side |
| `GET /v1/compare?a=&b=` | Question-level comparison over the union universe: `{a, b, counts: {questions_total, covered_a, covered_b, shared, agree, disagree}, shared[≤300]}`. Per shared question, each side's direction set is its members' distinct directions excluding `''`/`'none'`; the verdict is `agree` iff both sets are non-empty and equal, `disagree` iff both are non-empty and unequal, otherwise `null`. `truncated: true` is added when the shared list is capped. |

Three pages consume them, each through the `GC.d1(path)` helper in
`assets/app.js` (`fetch` against `https://api.guide.erbihou.org`, parsed JSON
on success, `null` on any failure — HTTP error, network error or bad JSON):

- `search.html` — `GC.d1('/v1/search?q=…')`; on `null`, loads
  `items.json / citations.json / questions.json` and filters client-side
  (items: statement/guideline/rec/topic_en/doc; citations:
  title/author/journal/pmid; questions: any member intervention/statement or
  the qid — all case-insensitive substring).
- `citation.html` — `GC.d1('/v1/citation?pmid=…')`; on `null`, rebuilds the
  same dossier from `citations.json ⋈ items.json`. A PMID present in
  `pmid_index.json` but absent from `citations.json` is reported as
  "indexed but unresolved", never as unknown.
- `compare.html` — guideline lists from `GC.d1('/v1/guidelines')` (fallback:
  derived from `items.json`); the comparison from
  `GC.d1('/v1/compare?a=&b=')` (fallback: the identical algorithm run over
  `questions.json` in the page — a Node harness verified worker and fallback
  produce byte-identical `shared` arrays on the frozen data). The frozen
  pair-level adjudicated aggregates in `compare.json` are displayed
  alongside, clearly labelled as a different unit.

`api.html` documents all ten endpoints publicly. Inbound links: citation
titles in `citations.html`, the looked-up title in `lookup.html` and pivotal
PMIDs in `explorer.html` now point at `citation.html?pmid=…`; `l4.html` and
`discordance.html` link to `compare.html`; `framework.html` and
`downloads.html` link to `api.html`.

`GC.resolveData` is deliberately unchanged: the v2 endpoints are additive
and each consuming page owns its fallback, so the static layer keeps working
verbatim whether the v1 or the v2 worker is deployed.
