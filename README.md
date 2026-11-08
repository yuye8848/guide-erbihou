# GuideCensus — public website

Source of https://guide.erbihou.org — the public face of the GuideCensus
five-layer census of the evidence beneath ENT clinical guideline
recommendations (46 documents, 805 current recommendations, frozen
2026-11-08).

Every number and data file on the site is generated from the frozen
datasets by `tools/build_data.py`; no statistic is hand-typed.
Regenerate with:

    python3 tools/build_data.py   # writes data/*.json + downloads/

Pages: five layer pages (L1–L5, colour-coded), a cross-filtering
recommendations explorer with shareable per-item URLs, PMID reverse
lookup (`lookup.html`), citation forward search by title / author /
year (`citations.html`, fed by `data/citations.json`), a discordance
deep-dive with a compare-two-guidelines view (`data/compare.json`),
the question universe, version dynamics, zombie watch, the
verification centre, and downloads. If a completed attachment-PMID
resolution lands in `data_resolution/attachment_pmid_index.csv`, the
build picks it up automatically and the lookup coverage rises.

All data access runs through `GC.load` / `GC.api` in `assets/app.js`;
see `INTEGRATION.md` for the single swap point that will point those
functions at the forthcoming D1-backed API without page changes.

Framework code and gold standard: https://github.com/yuye8848/guidecensus
Protocol and amendments: OSF 10.17605/OSF.IO/9VMFJ

Licences: data & documentation CC-BY-4.0; site code MIT.
