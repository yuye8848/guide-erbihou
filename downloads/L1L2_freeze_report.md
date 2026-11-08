# L1/L2 Freeze Report — D3 Guideline Evidence Census (2026-11-04)

**Freeze basis.** Protocol v1 (OSF 10.17605/OSF.IO/9VMFJ) §5/§8; Codebook
v0.1 §4 unified mapping; Amendments v1.1 (§A corpus, §C2), v1.2 (S1–S4);
conventions AC-1…AC-5. Analysis dataset: `analysis/frozen_dataset_l1l2.csv`
(sha256 29f9a476786d71ac…), merged from the 46 adjudicated Channel A files
(44 full-run incl. BPPV 2008 + 2 pilot). Cross-sectional layers (L1/L2)
use CURRENT versions only: **798 items / 31 documents**. The version
layer (379 items) is reserved for L5. Scripts retained per run:
`analysis/freeze_audit.py`, `analysis/l1l2_compute.py`,
`analysis/l1l2_extras.py`, `analysis/l2_logistic.R`; outputs
`analysis/l1l2_results.json`. Every number below traces to those files.

## 0. Freeze audit (machine scan, 2026-11-04)
- 46 files scanned; schemas identical (18 cols); **0 issues**: no
  duplicate rec_ids, no empty statements, no missingness-flag
  inconsistencies. Full value inventories in
  `analysis/freeze_audit_report.md`.
- **Total correction.** The census total is **1,177 items** (1,137
  full-run + 27 pilot + 13 BPPV 2008). The figure 1,150 used in the
  BPPV completion messages of 2026-11-04 omitted the pilot documents'
  27 items; corrected in the BPPV adjudication file, this report and
  MEMORY.md on the same day.
- Mapping rules applied (all logged in the audit report): first grade
  token for composite cells (AC-3.3/T3); printed "no data", "Grade X",
  "none", "N/A", "Uncertain", "Not applicable", "Unable to determine"
  = grade unrated (a result category); Oxford numeric levels 4 and 5
  map to U4 (Codebook §4 IV row); "Moderate-to-strong recommendation"
  (×2, ICAR RS 2021) mapped to the M rung with a sensitivity note;
  "Negative recommendation" (EAACI) = M against; "Opinion" (ICAR) = W.
  Zero unmapped values in the current-version set.

## 1. L1 — Composition (RQ1)
**Headline (S1): the share of recommendations backed by the highest
evidence tier (U1), per guideline, median = 12.2%** (IQR 0.0–26.6%;
guideline-level bootstrap 95% CI 6.3–21.4%). Pooled: 204/798 = 25.6%
(Wilson 95% CI 22.7–28.7%). The median sits inside the cardiology
benchmark band (8.5–14.2%, Tricoci/Fanaroff) and below Boesen's
weighted mean (15.9%); the pooled figure is higher because two large
documents are U1-rich (below). Ten of 31 documents have a U1 share
of exactly 0.

Pooled mapped distributions (n=798): evidence U1 204 (25.6%), U2 229
(28.7%), U3 301 (37.7%), U4 55 (6.9%), unrated 9 (1.1%). Strength:
S 124 (15.5%), M 380 (47.6%), W 221 (27.7%), no-recommendation/
unrated 73 (9.1%). Direction: for 617, against 106, none 75.
Strong-tier share: median 14.3% (bootstrap CI 10.2–25.0%); pooled
124/798 = 15.5%.

**Two disclosed mapping artefacts (dual-reporting rule applied):**
(i) EPOS 2020 is U1-dominated (68/71) because its summary tables
print Oxford level 1a/1b for nearly every intervention — a property
of the document (trial/SR-backed CRS pharmacotherapy dominates its
tables; only adenoidectomy/FESS-in-children print level 4 and one
no-evidence item level 5) — while its steering-group stances yield
zero S-tier strengths. (ii) EAACI 2018's S share (60%) is inflated by
its Box-2 phrasing code ("is recommended" = strong tier), disclosed
at extraction. Both are why the registered headline is the
per-guideline median, not the pooled share.

**Exploratory stratifications (S7 label):** by society — AAO U1 16.0%
(49/306), ICAR 16.9% (57/338), ARIA 0% (0/23), EAACI 50.0% (30/60),
EPOS 95.8% (68/71, artefact i). By topic: drug recommendations carry
the evidence (U1 47.2%, 162/343) while surgical recommendations
almost never do (U1 3.5%, 3/86); diagnostics U1 7.3% (13/177). By
type: treatment U1 36.8% vs diagnosis 7.3%. By population (derived
from the population field's age wording; 478 items state disease
only): children U1 39.5% (34/86), adults 43.1% (69/160), mixed 33.8%,
disease-only 15.9%.

## 2. L2 — Strength–evidence concordance (RQ2)
Qureshi operationalisation, implemented exactly (their Methods):
SOR ladder strong/moderate/weak/none; LOE ladder strong (U1) /
moderate (U2) / weak-or-very-weak (U3+U4) / none (unrated);
concordant iff LOE ≥ SOR; no-SOR items concordant by construction.

- **Overall concordance 69.0%** (551/798; Wilson 65.8–72.2%;
  guideline-cluster bootstrap 58.2–76.3%). Qureshi benchmark: 67.1%.
- Excluding no-SOR items (their sensitivity analysis): 65.9% (478/725).
- **Strong-only concordance 58.9%** (73/124; cluster CI 40.5–70.0%)
  vs Qureshi's 27%. Strong items' LOE mix: U1 58.9%, U2 27.4%,
  weak/very-weak 12.9%, unrated 0.8% (theirs: 27/34/20/20%). The ENT
  strong tier is far more evidence-coupled — structurally expected:
  AAO's own definitions tie "Strong recommendation" to grade A/B
  evidence, and ICAR aggregate grades skew high.
- Moderate-only concordance is the low cell: 48.9% (186/380) — the
  modal ENT cell is "Recommendation on grade C", which AAO's
  definitions permit but the Qureshi ladder scores as discordant.
  This is a property of applying a cross-specialty ladder to a
  proprietary system; reported with marginals, per S3.
- Weak-only concordance 99.1% (219/221).
- **κ (secondary, per S3):** Cohen's κ on the 4×4 rung table = 0.157
  (cluster-bootstrap 95% CI 0.05–0.25); quadratic-weighted κ = 0.151
  (−0.13–0.45). Exact-rung agreement is low because the modal
  evidence tier (U3) pairs with every strength tier — the marginals
  (4×4 table in l1l2_results.json) are displayed wherever κ appears.
  Qureshi's modified-κ formula (their ref 18) is not reconstructible
  from their article, and their κ values numerically coincide with
  their concordance proportions (0.67/27%); no κ-level cross-study
  claim is made.
- **Exploratory logistic model** (discordance among the 725 rated
  items; guideline-clustered robust SEs; R, cross-validated against
  the Python counts — discordant 247 in both implementations): vs
  AAO, discordance is lower for EPOS (OR ≈ 0.27), ICAR (≈ 0.40) and
  EAACI (≈ 0.54); treatment-type items are far less discordant than
  "other"-type items (OR ≈ 0.18); ARIA does not differ from AAO.
  Exploratory only (S7); not a headline.

## 3. §C2 — Discordance deepening (Amendment v1.1)
- **GRADE-native arm (ARIA 2025 R1+R2):** 7 strong items; exactly one
  item-level strong × very-low case — **ARIA2025R2-11**, second-
  generation over first-generation oral antihistamines, "strong
  recommendation based on very low certainty of evidence", panel's
  brief justification: "Second-generation OAH are safer and
  associated with higher patient satisfaction." Classified
  **paradigmatic** under Alexander 2016 / Agoritsas 2017: established
  harms of the comparator (sedation/anticholinergic effects of
  first-generation agents) with very-low certainty only on the
  comparative benefit. One further component-level case:
  **ARIA2025R1-01** (INAH+INCS over no treatment) is strong on
  moderate certainty for seasonal AR but **very low for perennial
  AR** (dual-certainty item; first-listed rule puts Moderate in
  grade_raw) — classified paradigmatic-pattern: benefit supported
  indirectly by the seasonal evidence, intervention harms rare and
  well characterised, alternative is no treatment.
- **AAO/ICAR arm:** strong recommendations resting on the lowest
  native tier (grade D) in current versions: **0 items** — the
  benefit–harm rationale transcription set is empty; the null is
  reported as the result.
- **EAACI disposition (disclosed):** EAACI 2018 is Oxford-adapted,
  not GRADE-native, so its 9 strong × weak-tier items are NOT forced
  into the Alexander taxonomy; they are also outside the AAO/ICAR
  transcription arm as specified. They are listed in the extras
  output: 8 of 9 are safety/practice-organisation statements (inform
  patients, control asthma before AIT, 30-minute observation,
  competent staff, SLIT reaction instructions) whose strong tier
  derives from the guideline's own Box-2 phrasing code — reported
  descriptively as good-practice-type statements.

## 4. External reconciliation
Full memo: `analysis/external_reconciliation_memo.md`.
- **Kaper 2020:** mapping structure isomorphic; both overlapping
  guidelines directionally consistent (AAO Sinusitis 2015 top-tier
  43% vs their High 38%; EPOS 2012 strong share identical at 41%);
  no mapping rule revised. Validation depth per Codebook §5 fallback
  (their harmonisation supplement was not obtainable).
- **Qureshi 2025:** their AAO-HNS sample = 7 documents / 107 items
  (2019–2023). Ours: 6 documents / 91 items by print year; 7 / 102
  including Age-Related Hearing Loss (online Dec 2023). Document
  count reconciles exactly under the e-publication dating; a
  residual 5-item gap is attributed to counting conventions.
  Supplement Table 2 (retrieved 2026-11-04 from PMC) reconciles
  closely: on the shared rated documents, SOR strong (17), SOR weak
  (11) and LOE strong (10) match EXACTLY, remaining rated cells
  differ by <=3 items; their +16 residual items are 14 doubly-
  unrated items from a seventh document whose ratings their
  ECRI-based extraction did not capture (identity not determinable
  from published materials; see memo).

## 5. Freeze statement
L1 and L2 as defined in Protocol v1 §8 and Amendments v1.1/v1.2 are
**FROZEN** as of 2026-11-04 on the dataset above. Any post-freeze
change requires a timestamped amendment. Next per the agreed
sequence: the two L3/L4 benchmarking memos, then L3/L4/L5.

## Re-freeze under Amendment v1.6 (2026-11-05)

One enumeration omission in ICAR: Rhinosinusitis 2021 was verified and
corrected (Amendment v1.6; memo
`l3_production/batch3/rs2021_suspected_missing3_verification_2026-11-05.md`):
item ICAR2021RS-82 (Oral Corticosteroids for CRSsNP; Option / Grade C)
inserted; two further suspected blocks (Herbal Medications for CRS,
Colloidal Silver for CRS) were re-verified as recorded policy-only
exclusions and NOT inserted. Re-run of freeze_audit + l1l2_compute +
l1l2_extras: census total 1,177 -> 1,178; cross-sectional denominator
798 -> 799 items / 31 documents; audit 0 issues. New frozen dataset
sha256 d952831e4f2468f9e0ada56e7d919cf6e659a05465836cd646ee3552de56deed
(this file supersedes the 2026-11-04 freeze; the superseded dataset,
results JSON and reports are archived unchanged in
`analysis/archive_freeze_2026-11-04/`). Headline deltas: U1 median
12.2% unchanged; pooled U1 204/798 = 25.6% -> 204/799 = 25.5%; L2
overall concordance 551/798 = 69.0% -> 552/799 = 69.1%; kappa
0.157 -> 0.158; strong-only concordance unchanged (73/124). The
inserted item is Channel-A-only and was not covered by human audit
pack #2; disclosed in Amendment v1.6.

## Re-freeze under Amendment v1.7 (2026-11-05)

The Amendment v1.6 §4 preventive enumeration diff was run on
ICAR-ESBS 2019 (HTML substrate) at the start of its L3 production
(memo `l3_production/batch3/esbs_enumdiff.md`): 66 EBRR blocks, 45
with a Policy/Recommendation Level line; the frozen 46 items
reverse-matched with zero orphans. Three Level-carrying blocks had
no L1 item and were verified as true omissions (Amendment v1.7):
ICAR2019ESBS-47 (EOND; Option / Grade C), ICAR2019ESBS-48
(free-graft reconstruction, block XI.A.2.d; Recommendation /
Grade C, policy-line anchored), ICAR2019ESBS-49 (lumbar drain,
block XI.A.2.e; Recommendation / Grade C, policy-line anchored).
One boundary block (V.A.6 JNA follow-up: Intervention statement but
no Level line) was recorded and NOT inserted, as the mirror image
of the v1.6 policy-only exclusions. Re-run of freeze_audit +
l1l2_compute + l1l2_extras: census total 1,178 -> 1,181;
cross-sectional denominator 799 -> 802 items / 31 documents; audit
0 issues. New frozen dataset sha256
6d64dd045a7127982c167f8d24d8865e92bf1c4acdbf6df4bc6ac7b1f12fef08
(supersedes d952831e...; the v1.6 dataset, results JSON and this
report's prior state are archived unchanged in
`analysis/archive_freeze_2026-11-05_v1.6/`). Headline deltas: U1
median 12.2% unchanged; pooled U1 204/799 = 25.5% -> 204/802 =
25.4%; drug 47.1% unchanged; surgical 3.5% -> 3.4% (3/88); L2
overall concordance 552/799 = 69.1% -> 553/802 = 69.0%;
strong-only unchanged (73/124); kappa 0.158 unchanged. The three
inserted items are Channel-A-only and were not covered by human
audit pack #2; disclosed in Amendment v1.7.

## Re-freeze under Amendment v1.8 (2026-11-05) — erratum

The batch-3 enumeration diff for ICAR-AR 2023 (memo
`l3_production/batch3/ar_prep/ar_enumdiff.md`; zero omissions, 79/79
items matched both directions, 185 AGE lines reconciled) flagged
one field error, verified by a column-aware re-read: ICAR2023AR-24
(Acoustic rhinometry) was frozen as Grade B; its block prints
"Aggregate grade of evidence: C" in the main text (layout
10396-10398). Grade B belongs to the adjacent Rhinomanometry block
(AR-23, correctly frozen). grade_raw corrected B -> C with an
erratum note on the row (Amendment v1.8). Re-run of freeze_audit +
l1l2_compute + l1l2_extras: totals unchanged (1,181 items; 802 /
31 documents); audit 0 issues. New frozen dataset sha256
5d7df323e9baf7fe17534ec05abcf273769ec609ef3be6d62bd7bc4b573ae0a3
(supersedes 6d64dd04...; v1.7 set archived unchanged in
`analysis/archive_freeze_2026-11-05_v1.7/`). Headlines: L1
unchanged (U1 median 12.2%, pooled 25.4%, drug 47.1%, surgical
3.4%); L2 concordance unchanged 553/802 = 69.0%; kappa 0.158 ->
0.160. The same diff recorded one boundary unit NOT inserted
(skin-testing drug-interference table X.B.4: graded directives but
no Policy/Recommendation Level line), per the standing inclusion
form (Amendment v1.8 §4).

## Re-freeze v1.9 (2026-11-05, Amendment v1.9 — ICAR-Olfaction 2022: three omitted blocks inserted on user ruling)

- Insertions (full_run/channelA/channelA_icar2022olf.csv, 49 → 52 rows; original IDs unchanged): ICAR2022OLF-50 oral corticosteroids for CRSsNP olfactory dysfunction (Option / Grade C; document position between OLF-17 and OLF-18) and the dual-policy Vitamin A block split in two — ICAR2022OLF-51 local application (Option / Grade C, for) and ICAR2022OLF-52 systemic (Recommendation / Grade C, against), both between OLF-42 and OLF-43, sharing the block's single printed aggregate C {2:1, 4:4}; the split follows this document's own block-39 PDEI precedent (OLF-45/46). One boundary block (phantosmia medical therapy, Table IX-40 — Aggregate + prose, no Policy/Intervention fields) recorded, NOT inserted. All three insertions are Channel-A-only and were NOT covered by §C1 audit pack #2 (disclosed in Amendment v1.9).
- Census: 46 documents / **1,184 items**; cross-sectional denominator **805 items / 31 documents**; freeze audit **0 issues**; frozen_dataset_l1l2.csv **sha256 92bf2294ec398b3d18bf5871fb1507a1dee34eaced883fcad1638cf46aa92574** (v1.8 set archived at analysis/archive_freeze_2026-11-05_v1.8/).
- L1 headlines (recomputed): U1 median **11.8%** (was 12.2% — the three non-U1 insertions dilute the OLF document share, shifting the cross-document median); pooled U1 **204/805 = 25.3%** (was 25.4%); drug **46.7% (162/347)** (was 47.1%); surgical unchanged 3.4% (3/88).
- L2 (recomputed): concordance **555/805 = 68.9%** (was 69.0%); κ **0.161** (was 0.160); strong-only unchanged 73/124.

## Freeze-stability comparison (assembled 2026-11-05 — supplementary-table draft for the manuscript)

Headline estimates at every L1/L2 freeze, taken verbatim from each freeze section above. Purpose: demonstrate that the four completeness/erratum re-freezes (Amendments v1.6–v1.9; 8 inserted items + 1 grade erratum = 9 of 1,184 records, 0.8%) did not move any headline estimate materially — and that every movement was slightly attenuating.

| Freeze | Cross-sectional denominator | U1 median | Pooled U1 | Concordance | κ | Strong-only |
|---|---|---|---|---|---|---|
| 2026-11-04 (original) | 798 | 12.2% | 204/798 = 25.6% | 551/798 = 69.0% | 0.157 | 73/124 |
| v1.6 (RS +1) | 799 | 12.2% | 204/799 = 25.5% | 552/799 = 69.1% | 0.158 | 73/124 |
| v1.7 (ESBS +3) | 802 | 12.2% | 204/802 = 25.4% | 553/802 = 69.0% | 0.158 | 73/124 |
| v1.8 (AR-24 erratum) | 802 | 12.2% | 204/802 = 25.4% | 553/802 = 69.0% | 0.160 | 73/124 |
| v1.9 (OLF +3) | 805 | 11.8% | 204/805 = 25.3% | 555/805 = 68.9% | 0.161 | 73/124 |

Largest absolute change, original → final: U1 median −0.4 pp; pooled U1 −0.3 pp; concordance −0.1 pp (peak-to-final −0.2 pp); κ +0.004; strong-only unchanged. No inclusion definition, outcome definition, or analysis changed at any re-freeze; all changes were enumeration completeness (blocks the protocol's own §4 audit gate found) or a single transcription erratum against the printed text.
