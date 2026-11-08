# GuideCensus — public website

Source of https://guide.erbihou.org — the public face of the GuideCensus
five-layer census of the evidence beneath ENT clinical guideline
recommendations (46 documents, 805 current recommendations, frozen
2026-11-08).

Every number and data file on the site is generated from the frozen
datasets by `tools/build_data.py`; no statistic is hand-typed.
Regenerate with:

    python3 tools/build_data.py   # writes data/*.json + downloads/

Framework code and gold standard: https://github.com/yuye8848/guidecensus
Protocol and amendments: OSF 10.17605/OSF.IO/9VMFJ

Licences: data & documentation CC-BY-4.0; site code MIT.
