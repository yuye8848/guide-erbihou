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
e.g. `return 'https://guide-api.erbihou.org/v1/' + name.replace(/\.json$/, '')`,
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
`assets/app.js` (`fetch` against `https://guide-api.erbihou.org`, parsed JSON
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

## Page changes (2026-11-08, user decision)

- `compare.html` **replaced** by `changes.html` ("What changed" — the L5
  direction flips and dropped recommendations, old wording against new;
  ARIA in its own section). The comparator was judged to carry no clinical
  meaning as a page. `compare.html` is now a redirect stub. The worker's
  `GET /v1/compare` endpoint and its `api.html` documentation are untouched
  (API surface only). The frozen pair-aggregate block that the comparator
  displayed now lives on `discordance.html` as a full table of
  `data/compare.json` (all 27 aligned document pairs), and the
  "compare any two guidelines live" link lines in `discordance.html` and
  `l4.html` were removed.
- `diseases.html` **added** ("Disease panorama"): the census re-sliced by
  the 20 disease areas of the L4 question universe — per area, question
  counts, current recommendations (joined from `items.json` via the frozen
  `parse_key` normalisation; prior-version / NICE member recs are counted
  as `unjoined_n`, never silently dropped), direction and pivotal-design
  breakdowns, fragile counts, and the area's L5 flips/dropped counts.
- New generated payloads, same frozen-data discipline (build scripts with
  assertions, no hand-typed statistics):
  - `data/changes.json` ← `tools/build_changes.py`, from
    `analysis/frozen_l5/phase1_alignment_final.csv` +
    `analysis/frozen_dataset_l1l2.csv` +
    `analysis/frozen_l5/l5_added_item_v23.csv`. The script recomputes the
    L5 Phase-1 headlines and asserts them against
    `analysis/frozen_l5/L5_freeze_report.md` (survival 359/390 = 92.1%
    excl. ARIA; flips 7/267; U up 58 / down 18 / same 246, n = 322;
    S strengthened 33 / weakened 4 / same 179, n = 216 — the tier summary
    is generated from the frozen grade/strength fields, not transcribed).
  - `data/diseases.json` ← `tools/build_diseases.py`, from
    `data/questions.json` + `data/items.json` + `data/changes.json`;
    per-area question counts are asserted against the frozen L4 coverage
    counts (20 areas).

## API hostname change (2026-11-09)

The `api.` custom domain never became reachable: its Advanced Certificate
stayed in "Pending Validation (Error)" (TXT validation, Google Trust
Services), so the edge had no valid certificate for the two-level hostname
`api.guide.erbihou.org` (the Universal certificate covers only one-level
`*.erbihou.org`). Removing and re-adding the custom domain on 2026-11-09 did
not clear the certificate state. By user decision the API hostname moved to
the one-level subdomain **`guide-api.erbihou.org`**, attached to the same
Worker `guide-api` as an additional custom domain (the `api.` domain remains
attached, unused). External acceptance on 2026-11-09 (parent-verified by
curl): `/v1/health` 200 `{"ok":true}`; `/v1/stats` items 805 / questions 905
/ citations 6,942 / links 10,243; `/v1/by-pmid`, `/v1/citation-search`,
`/v1/item`, `/v1/question` all 200 on live records. `GC.d1` in
`assets/app.js` and the endpoint examples in `api.html` now use the new
host; `GC.resolveData` remains static by design, and every `GC.d1` caller
keeps its static fallback.
