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
