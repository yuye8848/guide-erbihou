# L3 Freeze Report — D3 Guideline Evidence Census (2026-11-06)

> **SUPERSEDED IN PART by Amendment v2.0 (2026-11-06, §6 below).** The
> freeze declared in §5 (sha256 8493ba5f…) was audited by the
> pre-specified 10% audit pack, remediated corpus-wide, and **re-frozen
> the same day**: current frozen file sha256 **`e601a1a8…97fa`**, freeze
> audit **646/646 PASS**. §0–§5 and Appendix A/B describe the original
> freeze and stand as its record; **§6 carries the current totals** and
> governs wherever numbers differ.

> **FROZEN 2026-11-06.** The one item left open at draft stage —
> **ARIA2025R2-01**'s 5 B2 field checks — is closed by the supplement to
> `l3_production/b2_adjudication_batch5.md`: after three attempts the
> frozen verifier reproducibly returned a prose summary instead of
> verdicts for this single packet (the model-gated re-run's envelope
> confirms gemma3:27b), so those 5 checks are recorded as
> **B2-UNVERIFIED** and disclosed as such in §2. B2 is a flag-only
> channel and no row value was ever at issue for this item. With that
> disposition recorded, the freeze is declared below.

## 0. Freeze audit (machine scan, 2026-11-06)

Merge + audit script: `analysis/l3_freeze_audit.py` (rerunnable; it
reports mismatches, it never patches them). It assembles
`analysis/frozen_dataset_l3.csv` from the 31 final per-document
`*_L3_rows.csv` files (batches 1–5, post identity-slip corrections) in
batch → document → item-number order.

- **Checks run: 645 — PASS 645 / FAIL 0.**
- **Frozen file: `analysis/frozen_dataset_l3.csv`, sha256
  `8493ba5fa39484a9b0d8cbdfc0796330f7807906a0a65009e49ff05f3c41481c`**
  (re-running the audit reproduces the identical sha256).
- Audit coverage: per-document row counts vs the batch records (31/31);
  every source column mapped into the harmonised schema (31/31, no
  column dropped); designs-file merge conflicts (0); the batch 3–5
  statement/tier/grade consistency assertions against the frozen L1/L2
  dataset (499/499 rows); the frozen L1/L2 join for all 805 rows
  (511 exact + 294 normalised-id, key space collision-free); and the
  independent pivotal-design verification of every pivotal row against
  its owning designs file (**760 pivotal rows checked, 0 mismatches**).

### Harmonisation applied at merge (documented, asserted, reversible)

1. **Schema.** Target = the EPOS 19-column set. Batches 3–5 sources
   carry all 19 columns (identity mapping for the 16 production
   columns). Batches 1–2 sources carry only the 16 production columns;
   the remaining three (`statement`, `tier`, `evidence_grade`) are
   filled for **all 805 rows** from the frozen L1/L2 dataset
   (`statement_text` / `strength_raw` / `grade_raw`) via the rec_id
   join. This is exactly how batches 3–5 were built, asserted at merge:
   their stored `tier`/`evidence_grade` equal the frozen values
   verbatim (499/499) and their stored `statement` is the frozen text
   truncated to 110 characters (prefix relation, 499/499) — the frozen
   L3 file carries the full verbatim statement for every row.
2. **pivotal_design vocabulary** normalised into
   {SR/MA, RCT, primary, none}. The stored batch 1–2 vocabulary is
   fine-grained (cohort 34, case series 9, cross-sectional 5,
   case-control 1, diagnostic accuracy study 2, validation study 1,
   animal study 1, case report 1, observational 1, other 13, plus the
   RS file's 'other' 9 within batch 3's 13 'other' total — 68
   "other-specified" rows in the corrections memo's accounting) and 15
   rows store a blank. Mapping rule: a row with a pivotal_ref whose
   design is not SR/MA/RCT is a **primary** pivotal; a row with no
   pivotal_ref and a blank stored value is **none**. All 83 non-obvious
   mappings are listed per-row in Appendix A, each with the
   designs-file design that independently confirms the class.
3. **Kept verbatim (not harmonised), disclosed:** 13 pivotal-none rows
   (8 batch-1 + 5 ICAR-RS) store blank `applicability`/`surrogate`
   rather than the direct/no coding used elsewhere; 6 AAO2019SHL rows
   store a blank `pivotal_n` whose own `pivotal_n_source` reads
   'unavailable'. Both wrinkles are preserved as stored and accounted
   in §1.

## 1. Corpus totals (frozen)

| Quantity | Value |
|---|---|
| Documents | 31 |
| Items (rows) | 805 |
| Citation attachments (Σ citations_n) | 11,571 |
| RCT attachments | 2,556 |
| SR/MA attachments | 1,392 |
| Items with ≥1 SR/MA (has_srma = yes) | 462 |
| Pivotals — SR/MA | 376 |
| Pivotals — RCT | 239 |
| Pivotals — primary | 145 (= 77 stored 'primary' + 68 fine-grained) |
| Pivotals — none | 45 (= 30 stored 'none' + 15 blank) |
| Pivotal N verified / unavailable | 385 / 420 (see definition note) |
| Applicability — direct / indirect / blank | 716 / 76 / 13 |
| Surrogate — no / yes / blank | 768 / 24 / 13 |

**Pivotal-N definition note.** "Verified 385 / unavailable 420" uses
the operational definition of the identity-slip corrections memo:
verified := `pivotal_n` is not the literal string 'unavailable'. The
strict composition is: numeric N stated **364**, literal 'unavailable'
**420**, blank **21** — of the blanks, 15 are pivotal-none rows (no N
exists to verify) and 6 are the AAO2019SHL rows noted in §0. Both
accountings are printed by the audit script on every run.

### Per-document table

Rows / attachments (Att) / RCT attachments / SR/MA attachments /
pivotals SR/MA·RCT·primary·none / pivotal N verified·unavailable
(corrections-memo definition).

| Document | Batch | Rows | Att | RCT att | SR/MA att | Pivotals | N v/u |
|---|---|---:|---:|---:|---:|---|---|
| AAO2013BELL | 1 | 13 | 143 | 19 | 24 | 5/3/5/0 | 9/4 |
| AAO2013VOICE | 1 | 13 | 278 | 13 | 9 | 4/5/4/0 | 11/2 |
| AAO2014AOE | 1 | 8 | 143 | 18 | 7 | 1/3/3/1 | 4/4 |
| AAO2014TIN | 1 | 14 | 252 | 41 | 32 | 10/2/2/0 | 6/8 |
| AAO2015AR | 1 | 14 | 355 | 145 | 54 | 7/5/1/1 | 8/6 |
| AAO2016OME | 1 | 18 | 289 | 35 | 63 | 15/0/3/0 | 1/17 |
| AAO2017BPPV | 1 | 14 | 348 | 56 | 30 | 9/4/1/0 | 5/9 |
| AAO2017CER | 1 | 15 | 147 | 19 | 9 | 4/6/5/0 | 7/8 |
| AAO2017NECK | 1 | 12 | 113 | 3 | 9 | 3/2/5/2 | 6/6 |
| AAO2017RHINO | 1 | 10 | 106 | 19 | 22 | 3/5/2/0 | 4/6 |
| AAO2018HOARSE | 1 | 15 | 425 | 34 | 24 | 5/4/6/0 | 2/13 |
| AAO2019SHL | 1 | 14 | 314 | 30 | 22 | 3/4/6/1 | 14/0 |
| AAO2020EPI | 1 | 16 | 187 | 17 | 18 | 5/7/4/0 | 9/7 |
| AAO2020MEN | 1 | 17 | 370 | 35 | 27 | 6/7/3/1 | 8/9 |
| AAO2021OPI | 1 | 12 | 247 | 31 | 31 | 9/2/0/1 | 6/6 |
| AAO2022TYMP | 1 | 16 | 326 | 50 | 52 | 9/6/1/0 | 5/11 |
| AAO2024ARHL | 1 | 11 | 175 | 8 | 25 | 4/3/4/0 | 3/8 |
| AAO2025CRS | 1 | 12 | 286 | 17 | 31 | 8/2/2/0 | 2/10 |
| AAO2025SIN2 | 1 | 17 | 391 | 25 | 61 | 11/3/2/1 | 10/7 |
| AAO2019TONS | 2 | 16 | 268 | 44 | 49 | 10/5/0/1 | 6/10 |
| AAO2024AIT | 2 | 13 | 236 | 38 | 34 | 5/7/0/1 | 6/7 |
| AAO2026TIN2 | 2 | 16 | 375 | 63 | 97 | 13/3/0/0 | 11/5 |
| ICAR2019ESBS | 3 | 49 | 662 | 18 | 62 | 30/5/14/0 | 27/22 |
| ICAR2021RS | 3 | 82 | 849 | 235 | 69 | 30/38/9/5 | 63/19 |
| ICAR2022OLF | 3 | 52 | 544 | 114 | 32 | 16/19/17/0 | 20/32 |
| ICAR2023AR | 3 | 79 | 1,365 | 560 | 279 | 43/23/11/2 | 26/53 |
| ICAR2024TUM | 3 | 83 | 1,333 | 49 | 144 | 43/5/32/3 | 37/46 |
| EPOS2020 | 4 | 71 | 287 | 224 | 25 | 21/48/0/2 | 57/14 |
| ARIA2025R1 | 5 | 11 | 0 | 0 | 0 | 0/0/0/11 | 0/11 |
| ARIA2025R2 | 5 | 12 | 10 | 0 | 5 | 3/0/0/9 | 1/11 |
| EAACI2018 | 5 | 60 | 747 | 596 | 46 | 41/13/3/3 | 11/49 |
| **Corpus** | | **805** | **11,571** | **2,556** | **1,392** | **376/239/145/45** | **385/420** |

(AAO2019SHL's 14/0 is the memo definition at work: its 6 blank-N rows
count as verified there; strictly, 7 of its pivotals state a numeric N
and 6 carry source = 'unavailable'. ARIA2025R1's zero attachments are a
substrate fact — its brief justifications cite nothing; the evidence
sits in the online-only EtD frameworks.)

## 2. B2 verification summary (frozen verifier, Gemma3-27B; flag-only channel)

Every challenge in every batch was adjudicated in writing against the
source text; verifier corrections were never auto-applied. **Across
4,020 adjudicated field checks, 359 challenges were raised and 0 were
upheld** — no L3 row value in any batch was changed by B2.

| Batch | Documents | Checks | CONFIRM | CHALLENGE | CANNOT_VERIFY | Upheld |
|---|---|---:|---:|---:|---:|---:|
| 1 | 19 AAO | 1,305 | 1,201 | 96 | 8 | 0 |
| 2 | TONS / AIT / TIN2 | 225 | 215 | 10 | 0 | 0 |
| 3 | ICAR RS / ESBS / OLF / TUM / AR | 1,725 | 1,471 | 185 | 69 | 0 |
| 4 | EPOS 2020 | 355 | 320 | 32 | 3 | 0 |
| 5 | ARIA R1/R2 + EAACI 2018 | 410 | 369 | 36 | 5 | 0 |
| **Total adjudicated** | **31** | **4,020** | **3,576** | **359** | **85** | **0** |

> **Batch-5 supplement — closed as B2-UNVERIFIED (2026-11-06):**
> ARIA2025R2-01's 5 field checks are not in the table above and never
> entered adjudication. In the original batch-5 run the verifier went
> off-task on this single packet (prose summary, no verdicts —
> established by raw-file audit); a first re-run was invalidated
> because the notebook copy ran a non-frozen model (qwen3:8b); the
> model-gated re-run under the frozen Gemma3-27B (envelope model
> confirmed on retrieval) again returned a prose summary with no
> verdicts. The 5 checks are therefore recorded as B2-UNVERIFIED — a
> channel limitation specific to this packet, disclosed here and in
> the supplement to `l3_production/b2_adjudication_batch5.md`. The
> item's claims were re-derived byte-identically from the final rows
> at bundle build (83/83 packets). Corpus-wide, 5 of 4,025 attempted
> B2 checks (0.12%) are unverified, all belonging to this one item.

Adjudication files: `l3_production/b2_adjudication_batch1.md`,
`l3_production/batch2/b2_adjudication_batch2.md` (+ 2026-11-06
postscript), `l3_production/b2_adjudication_batch3_{rs,esbs,olf,tum,ar}.md`,
`l3_production/b2_adjudication_batch4_epos.md`,
`l3_production/b2_adjudication_batch5.md`.

## 3. Closeout components

- **Corpus-wide retraction / withdrawal check** (`closeout/retraction_check_memo.md`):
  4,605 unique corpus PMIDs checked, **CHECK_FAILED 0**. CLEAR 4,116 ·
  CORRECTION_ONLY 493 · **WITHDRAWN 3** (the SIN2-KAS12 pivotal
  Cochrane review PMID 30184244; the EPOS-16 zinc review CD001364; the
  EPOS-69 saline review CD006394 — the latter two are pivotals,
  adjudicated normally from their cited versions and flagged) ·
  **RETRACTED 1** (PMID 37062296, Jiang 2023 hearing-aid/dementia —
  an attachment in ARHL KAS02/KAS06, not a pivotal) · **EXPRESSION OF
  CONCERN 1 citation** (VIGOR, PMID 11087881 — an attachment in
  OPI-KAS06, not a pivotal). Pivotal coverage 746/760 instances
  (98.2%); the 14 uncovered instances (12 unique citations without a
  PMID) are listed by name in the memo — their status is unknown, not
  clear.
- **OpenAlex citation pull** (`closeout/openalex_memo.md`), retrieved
  2026-11-06: 4,605 PMIDs → **4,585 found / 20 not found / 0 failed**.
  All found corpus works: median cited_by 54 (IQR 25–116). Pivotal
  works (592 unique): median 55 (IQR 25–128). Counts are as-of
  retrieval.
- **10% human audit pack** (`closeout/audit_pack/`): 81 items (10.06%)
  sampled stratified by document (every document ≥2), seed 20261106,
  draw reproduced byte-identically in an independent re-run (selection
  sha256 `7aed1dd7…`); each sampled item ships with its B2 packet and
  blank auditor columns. The pack is prepared and frozen with the
  dataset; the human audit itself sits outside production.

## 4. Identity-slip correction note (applied 2026-11-06, pre-freeze)

During the retraction check, 11 citation-identity slips were found in
production's stored matches (matches latched onto errata/commentary
derivative records). Six carried design consequences; all six were
corrected with mirror-validated scripts and pre-correction backups
(`closeout/identity_slip_impact_memo.md`,
`closeout/identity_slip_corrections_applied.md`): exactly **9 rows
changed** — 8 counts-only (+4 SR/MA and +5 RCT attachments corpus-wide)
and **1 pivotal swap** (AAO2024AIT-KAS01: ref 65 → ref 64, the Dhami
2017 EAACI SR/MA; N unavailable on both sides). Postscripts were
appended to the affected batches' B2 adjudications per the batch-3 RS
precedent (B2 verified the pre-correction claims; the as-run records
stand). The corpus totals in §1 are the post-correction totals, and
the freeze audit above verifies them from the files on disk.

## 5. Freeze statement

The L3 dataset is frozen as
`analysis/frozen_dataset_l3.csv` (805 items, 31 documents, sha256
`8493ba5f…c41481c`), assembled and audited by
`analysis/l3_freeze_audit.py` with 645/645 checks passing. Any future
change follows the L1/L2 pattern: a timestamped amendment, a re-run of
the audit, and a new sha256 recorded here.

## 6. Amendment v2.0 — post-freeze audit, remediation, RE-FREEZE (2026-11-06)

Full text: `protocol/Protocol_v2.0_amendment_2026-11-06.md`. Summary:

The pre-specified 10% audit pack (81 items, seed 20261106) was executed
as an **independent AI audit** (four auditors with no production
involvement; every disagreement adjudicated against source text and
Europe PMC) and, by the corresponding author's ruling of 2026-11-06,
stands as the **audit of record** — reported as an AI audit, never as a
human audit (author reviewed the findings and approved all
corrections). Outcome: 75 field rulings, 60 upheld; 40/81 items
(49.4%) carried ≥1 upheld correction (field-level 60/405 = 14.8%).
Dominant classes: roster omissions from 'unverified' designs,
pivotal_n errors (19), identity slips, set-construction misses, one
phantom-citation item (AAO2021OPI-KAS10).

The author ordered a full-corpus remediation (sweeps S1–S5 over all
805 items; every proposed change adjudicated; unverifiable values
recorded as such, never inferred). Applied as one amendment:
349 designs records changed (S2: 316 adjudicated re-classifications of
718 'unverified' refs — SR/MA 49 / RCT 49 / other 218, 397 refs
confirmed record-less; audit calls: 33), 4 items' sets changed,
**13 pivotal displacements** (audit 7 + S4 6), **119 rows' pivotal_n
changed** (S3: 109 net corrections from full-abstract re-verification
of 760 pivotal instances). 247 of 805 items carry ≥1 changed field.

Verification on the amended state: S1 re-derivation 0 diffs; audit-81
reconciliation 0 hard failures (2 documented S2-layer additions on
fields the audit never ruled on); **freeze audit 646/646 PASS**
(`analysis/l3_freeze_audit.py`; its EXPECT block now carries the
amended totals).

**Current corpus totals (supersede §1):**

| Quantity | Value (Δ vs §1) |
|---|---|
| Documents / items | 31 / 805 |
| Citation attachments | 11,567 (−4) |
| RCT attachments | 2,640 (+84) |
| SR/MA attachments | 1,472 (+80) |
| Pivotals — SR/MA / RCT / primary / none | 376 / 238 / 145 / 46 |
| Pivotal N verified / unavailable | 481 / 324 (strict numeric 460) |

**RE-FREEZE STATEMENT.** The L3 dataset is re-frozen as
`analysis/frozen_dataset_l3.csv` (805 items, 31 documents), sha256
`e601a1a8b6998563224207b0c4132fb2ef3bccdd3d0c959e7af3bf29091297fa`,
superseding 8493ba5f…. Carried-unresolved items (no values fabricated)
are listed in Amendment v2.0 §4. L4/L5 are computed from this file.

## Appendix A — Non-obvious pivotal_design mappings (83 rows)

Stored fine-grained labels → 'primary' (68 rows) and stored blanks →
'none' (15 rows). The 'designs' column is the owning designs file's
design for the pivotal ref — the independent confirmation of the
mapped class (SR/MA/RCT claims are verified the same way but are not
listed here, being vocabulary-identical).

| rec_id | stored | ref | designs | resolution |
|---|---|---|---|---|
| AAO2013BELL-KAS01 | 'cohort' | 1 | other | → 'primary' |
| AAO2013BELL-KAS02 | 'observational' | 52 | other | → 'primary' |
| AAO2013BELL-KAS07A | 'cohort' | 21 | other | → 'primary' |
| AAO2013BELL-KAS07B | 'cohort' | 97 | other | → 'primary' |
| AAO2013BELL-KAS11 | 'cohort' | 1 | other | → 'primary' |
| AAO2013VOICE-KAS01 | 'cohort' | 70 | other | → 'primary' |
| AAO2013VOICE-KAS02A | 'cohort' | 38 | other | → 'primary' |
| AAO2013VOICE-KAS02B | 'cohort' | 38 | other | → 'primary' |
| AAO2013VOICE-KAS05 | 'cohort' | 152 | other | → 'primary' |
| AAO2014AOE-KAS01 | '' (blank) | - | - | → 'none' |
| AAO2014AOE-KAS02 | 'case series' | 75 | other | → 'primary' |
| AAO2014AOE-KAS03 | 'validation study' | 92 | other | → 'primary' |
| AAO2014AOE-KAS07 | 'animal study' | 149 | other | → 'primary' |
| AAO2014TIN-KAS02B | 'cohort' | 77 | other | → 'primary' |
| AAO2014TIN-KAS04 | 'cross-sectional' | 105 | other | → 'primary' |
| AAO2015AR-KAS01 | '' (blank) | - | - | → 'none' |
| AAO2015AR-KAS03 | 'cohort' | 58 | other | → 'primary' |
| AAO2016OME-KAS03 | 'cohort' | 85 | other | → 'primary' |
| AAO2016OME-KAS04A | 'case series' | 97 | other | → 'primary' |
| AAO2016OME-KAS04B | 'case series' | 97 | other | → 'primary' |
| AAO2017BPPV-KAS03B | 'case series' | 147 | other | → 'primary' |
| AAO2017CER-KAS02A | 'cross-sectional' | 3 | other | → 'primary' |
| AAO2017CER-KAS02B | 'case series' | 49 | other | → 'primary' |
| AAO2017CER-KAS04 | 'cohort' | 79 | other | → 'primary' |
| AAO2017CER-KAS05B | 'case report' | 97 | other | → 'primary' |
| AAO2017CER-KAS10 | 'cohort' | 107 | other | → 'primary' |
| AAO2017NECK-KAS02A | '' (blank) | - | - | → 'none' |
| AAO2017NECK-KAS02B | 'diagnostic accuracy study | 70 | other | → 'primary' |
| AAO2017NECK-KAS02C | 'case series' | 6 | other | → 'primary' |
| AAO2017NECK-KAS03 | 'cohort' | 21 | other | → 'primary' |
| AAO2017NECK-KAS05 | 'cohort' | 85 | other | → 'primary' |
| AAO2017NECK-KAS09 | '' (blank) | - | - | → 'none' |
| AAO2017NECK-KAS10 | 'cohort' | 96 | other | → 'primary' |
| AAO2017RHINO-KAS01 | 'cross-sectional' | 5 | other | → 'primary' |
| AAO2017RHINO-KAS07 | 'case series' | 27 | other | → 'primary' |
| AAO2018HOARSE-KAS01 | 'cohort' | 97 | other | → 'primary' |
| AAO2018HOARSE-KAS02 | 'case-control' | 105 | other | → 'primary' |
| AAO2018HOARSE-KAS04A | 'case series' | 161 | other | → 'primary' |
| AAO2018HOARSE-KAS04B | 'cohort' | 122 | other | → 'primary' |
| AAO2018HOARSE-KAS05 | 'cohort' | 197 | other | → 'primary' |
| AAO2018HOARSE-KAS09A | 'cohort' | 135 | other | → 'primary' |
| AAO2019SHL-01 | '' (blank) | - | - | → 'none' |
| AAO2019SHL-02 | 'cohort' | 12 | other | → 'primary' |
| AAO2019SHL-03 | 'other' | 49 | other | → 'primary' |
| AAO2019SHL-04 | 'other' | 84 | other | → 'primary' |
| AAO2019SHL-05 | 'other' | 49 | other | → 'primary' |
| AAO2019SHL-06 | 'cohort' | 105 | other | → 'primary' |
| AAO2019SHL-07 | 'other' | 141 | other | → 'primary' |
| AAO2020EPI-KAS04 | 'cohort' | 69 | other | → 'primary' |
| AAO2020EPI-KAS06 | 'diagnostic accuracy study | 82 | other | → 'primary' |
| AAO2020EPI-KAS07A | 'cohort' | 85 | unverified | → 'primary' |
| AAO2020EPI-KAS07B | 'cohort' | 85 | unverified | → 'primary' |
| AAO2020MEN-KAS01 | '' (blank) | - | - | → 'none' |
| AAO2020MEN-KAS02 | 'case series' | 73 | other | → 'primary' |
| AAO2020MEN-KAS04 | 'cohort' | 112 | other | → 'primary' |
| AAO2020MEN-KAS15 | 'cohort' | 376 | other | → 'primary' |
| AAO2021OPI-KAS08A | '' (blank) | - | - | → 'none' |
| AAO2022TYMP-KAS08 | 'cross-sectional' | 159 | other | → 'primary' |
| AAO2024ARHL-KAS04 | 'cohort' | 123 | other | → 'primary' |
| AAO2024ARHL-KAS05 | 'cohort' | 168 | other | → 'primary' |
| AAO2024ARHL-KAS10 | 'cross-sectional' | 120 | other | → 'primary' |
| AAO2024ARHL-KAS11 | 'cohort' | 263 | other | → 'primary' |
| AAO2025CRS-KAS01A | 'cohort' | 91 | other | → 'primary' |
| AAO2025CRS-KAS01B | 'cohort' | 91 | other | → 'primary' |
| AAO2025SIN2-KAS01B | 'cohort' | 66 | other | → 'primary' |
| AAO2025SIN2-KAS10 | 'cohort' | 340 | other | → 'primary' |
| AAO2025SIN2-KAS13A | '' (blank) | - | - | → 'none' |
| AAO2019TONS-KAS14 | '' (blank) | - | - | → 'none' |
| AAO2024AIT-KAS09 | '' (blank) | - | - | → 'none' |
| ICAR2021RS-01 | 'other' | 299 | other | → 'primary' |
| ICAR2021RS-02 | 'other' | 216 | other | → 'primary' |
| ICAR2021RS-11 | '' (blank) | - | - | → 'none' |
| ICAR2021RS-12 | 'other' | 497 | other | → 'primary' |
| ICAR2021RS-16 | 'other' | 525 | other | → 'primary' |
| ICAR2021RS-20 | 'other' | 40 | other | → 'primary' |
| ICAR2021RS-27 | 'other' | 1128 | other | → 'primary' |
| ICAR2021RS-57 | '' (blank) | - | - | → 'none' |
| ICAR2021RS-61 | '' (blank) | - | - | → 'none' |
| ICAR2021RS-62 | '' (blank) | - | - | → 'none' |
| ICAR2021RS-63 | 'other' | 1929 | other | → 'primary' |
| ICAR2021RS-69 | 'other' | 1780 | other | → 'primary' |
| ICAR2021RS-77 | 'other' | 2231 | other | → 'primary' |
| ICAR2021RS-81 | '' (blank) | - | - | → 'none' |

## Appendix B — Flagged resolutions and verbatim-kept wrinkles

1. **AAO2020EPI-KAS07A / KAS07B** — pivotal ref 85's designs-file entry
   reads 'unverified'. The rows' own adjudicated §2 label ('cohort')
   governs; under the mapping rule the class resolves to 'primary'.
   Disclosed here rather than silently absorbed: the pivotal's design
   rests on the row's adjudication label, not on a verified designs
   record.
2. **Blank applicability/surrogate (13 rows, kept verbatim):**
   AAO2014AOE-KAS01, AAO2015AR-KAS01, AAO2017NECK-KAS02A,
   AAO2017NECK-KAS09, AAO2019SHL-01, AAO2020MEN-KAS01,
   AAO2021OPI-KAS08A, AAO2025SIN2-KAS13A, ICAR2021RS-11,
   ICAR2021RS-57, ICAR2021RS-61, ICAR2021RS-62, ICAR2021RS-81 — all
   pivotal-none rows whose batch adjudications left the two fields
   blank instead of coding direct/no.
3. **AAO2019SHL blank pivotal_n (6 rows: -03, -04, -05, -06, -07,
   -13)** — `pivotal_n` blank with `pivotal_n_source` = 'unavailable';
   kept verbatim. Under the strict accounting these 6 are unavailable;
   under the corrections-memo definition they fall in the 385.
4. **EAACI2018 unverified citations 136 and 190** have no entry in the
   designs file by construction (no Europe PMC record after four query
   strategies); they are attachments in items -33/-34 and -51, never
   pivotals, and count as neither RCT nor SR/MA in their rows.
5. **ARIA2025R1 has no designs file** — its 11 items attach zero
   citations (substrate fact, §1), so there is nothing to classify.

## Amendment v2.5 re-freeze (2026-11-08)

Post-freeze verification under Amendment v2.4 §S3b measured residual
pivotal-field errors of 7.3% (identity) and 7.3% (design) in a 41-item
independent sample — above the pre-stated 5% threshold. The user ordered
FULL remediation (Amendment v2.5, filed on OSF before any data touch).
This dataset file is re-issued: **sha256
2785235daca0aca22bf76865b7a8cf05803a3984991430b7e3c2ccf54c94f7fd**
(v2.0 file archived unchanged at
analysis/archive_v20/frozen_dataset_l3_v20_e601a1a8.csv; mirrored to VPS2
and VPS3 at /root/d3_l3_freeze_v25/, hashes verified).

What changed (254 of 805 items carry at least one changed cell; statement /
tier / evidence_grade / citations_n are byte-identical to v2.0 throughout):
- Integrity sweep of all 4,615 title-bearing designs-artefact entries
  against the documents' own reference lists: 293 mismatches; 169
  re-resolved through the frozen strict gates (146 identities replaced, 23
  rendering variants confirmed), 124 corrected to 'unverified' with the
  gates unrelaxed. Candidate rosters (rct_refs / srma_refs / counts /
  pivotal_candidate) recomputed from the corrected rosters in span order.
- Pivotal re-derivation on the verified rosters for the 151 operatively
  affected items: 129 stand; 22 proposals changed the pivotal — 21 accepted
  by written parent adjudication, 1 rejected on the F3 screen
  (ICAR2021RS-56); plus AAO2020MEN-KAS13 corrected via the S3b sample
  clause. All 14 S3b-adjudicated field corrections are incorporated.
- pivotal_n retrieval-depth clarification (v2.5): stated totals were
  completed from full text/tables for the 299 in-scope items; 62 of 66
  found totals passed a triple identity guard and were applied, 2 were
  rejected as wrong-record totals, 2 reached the item through reselection.
- **Pivotal composition: SR/MA 375 / RCT 233 / primary 151 / none 46**
  (v2.0: 376 / 238 / 145 / 46). pivotal_n numeric 520 / 'unavailable' 266 /
  blank 19 (v2.0 raw column: 460 / 324 / 21).
- Version rulings (parent, on printed citations + fetched records):
  EPOS2020-16's pivotal is the cited 2011 zinc record (PMID 21328251,
  n=1360) — its frozen zombie determination is WITHDRAWN (the withdrawn
  record is the uncited 2015 update); ICAR2021RS-29's Head 2018 review
  (PMID 30199594) is a different review from the withdrawn Sacks record
  and is NOT a zombie; AAO2025SIN2-KAS12's Sacks pivotal (PMID 30184244)
  remains a zombie. **Zombie pivotals: 2** (see the L5 addendum).
Full artefacts: l3_production/remediation_v25/ (integrity report,
reselection proposals, parent adjudication, merge diff, downstream
recomputation). Post-remediation verification (fresh 41-item sample, seed
20261109) is reported in the v2.5 report.

### v2.5 verification-round corrections (2026-11-08, post-re-freeze)

The §7 post-remediation verification (fresh 41-item sample, seed 20261109,
independent blind re-derivation; parent adjudication at
l3_production/remediation_v25/verify_v25/parent_adjudication.md) upheld:
pivotal identity 1/40 = 2.5% and pivotal design 0/41 — both within the
pre-stated 5% limits, so the remediation stands. Seven adjudicated
corrections were applied to the re-issued file (ICAR2021RS-73 pivotal
2058→2043 Hudon 2018; six pivotal_n corrections incl. AAO2020EPI-KAS09
830→'unavailable', a pooled-subset value). **Final v2.5 file: sha256
cebf5e51b110248d1a66376ed0848f40e31b8f5a652fbe9fe0ea6999393f2313**
(intermediate 2785235d… retained at
l3_production/remediation_v25/frozen_dataset_l3_v25_final.csv's predecessor
copy in the remediation folder; mirrored to VPS2/VPS3, hashes verified).
Disclosed residual: numeric pivotal_n values carrying subset/completer
counts (3 of ~14 checkable numeric values in the verification sample)
were outside the completion sweep's scope; see the v2.5 report.

### Numeric pivotal_n sweep (v2.5 addendum, 2026-11-08) — final re-issue

Per the OSF-filed addendum, all 522 numeric pivotal_n values were verified
against their pivotal records (abstract stage + full-text stage). Outcome:
497 confirmed, 19 errors upheld and corrected (16 numeric→numeric; 3 →
'unavailable' where the frozen value's basis — meta-analysis comparison
arms, an overlapping comparison-subset total, a tumour count — was
demonstrated impermissible and no qualifying total exists), 6 not verified
(frozen values stand, listed in the sweep report). **One correction REVERTS
a v2.5 verification-round change: AAO2019TONS-KAS03 returns to 26** — the
39 applied earlier rested on a quote from a different trial; the pivotal
(Renko 2007, PMID 17719940) states 26. Record-verified by the parent;
adjudication at l3_production/remediation_v25/numeric_sweep/.
**Final file: sha256 db769136a5bc0ebde77fa8c9f38298a6fecaf2ddd5e9e56c5a251aa240e8a75d**
(pivotal_n numeric 519; median 216; N<400 312 — no frozen report prints
pivotal_n-dependent figures, so no other document changes). Mirrored to
VPS2/VPS3, hashes verified.
