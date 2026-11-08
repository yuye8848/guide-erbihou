# L5 Freeze Report — Version Dynamics (2026-11-08)

**Status: L5 FROZEN.** Method: Protocol Amendment v2.2 + Phase-2 addendum +
Amendment v2.3 (Adult Sinusitis 2007 Statement #9), all filed on OSF
(10.17605/OSF.IO/9VMFJ) before their respective data touches. Frozen L1/L2/L3/L4
files are untouched by L5. Freeze set: `analysis/frozen_l5/` (21 files incl.
this report; hashes in `freeze_sha256.txt`).

## Scope

16 version transitions, 14 families: 15 prior documents (380 items after v2.3)
plus the tinnitus pair (AAO 2014 → AAO 2026, per the v2.2 §4 ruling; AAO 2014
remains 'current' in the frozen L1–L4 denominators — disclosed here and owed
in the manuscript).

## Phase 1 — recommendation dynamics (frozen L1/L2 fields only)

- Alignment: 394 rulings — carried-identical 130 / carried-modified 231 /
  dropped 33. Independent blind check (46 packets): verdict agreement 78.3%;
  21 changes applied on written parent adjudication
  (`phase1_adjudication_log.md`).
- Pooled survival (15 transitions excl. ARIA): **359/390 = 92.1%**
  [Wilson 88.9–94.3].
- Direction flips among both-stanced carried pairs: **7/267 = 2.6%**.
- Evidence tier (U): up 58 / down 18 / same 246 (n=322). Strength (S/M/W):
  strengthened 33 / weakened 4 / same 179 (n=216).
- ARIA T15 reported separately throughout (partial lineage; its 2025 side has
  two documents; prior side has no item-level apparatus): survival 2/4.

## Phase 2 — citation dynamics

- Prior attachment extraction: 4,608 rows = 4,570 real attachments + 38
  documented no-reference marker rows over 380 items; deduplicated to 3,073
  unique studies; identity-matched 2,686 (87.4%), unverified 386, unfetched 1.
  Designs among matched: SR/MA 222 / RCT 725 / other 1,739.
- Current-side per-item attachment sets were reconstructed from the L3
  channel-A artefacts and verified against the frozen L3 library: all 395
  transition-relevant items / 5,785 attachments reproduce exactly.
- **Document-level citation turnover: 0.662 pooled** (1 − 1,690/5,002);
  transition range 0.364 (BPPV 2008→2017) to 0.804 (Tinnitus 2014→2026).
- **Item-level turnover over carried pairs: 0.678 pooled** (356 pairs;
  3 excluded for empty current sets).
- **Pivotal persistence: 57/292 = 19.5%** of carried pairs with a pivotal
  resolved on both sides keep the same pivotal study (7 further pairs
  excluded for an unresolved pivotal identity on one side).

## Zombie citations (three pre-specified strata, never pooled)

- **(b) Current-version pivotals: 3 zombies / 586 screened PMIDs** — all
  Cochrane reviews withdrawn years before the citing guideline: PMID 30184244
  (withdrawn 2018; pivotal of AAO2025SIN2-KAS12), PMID 25924708 (2015;
  EPOS2020-16), PMID 27110699 (2016; EPOS2020-69).
- **(a) Persistent attachments (in both versions of a transition): 0 zombies
  / 1,406 screened PMIDs** (none_found 1,406; unfetched 0; verified by an
  independent raw-signal rescan of the fetch checkpoint).
- **(c) Closeout-flagged records, individually verified: 1 zombie
  attachment** — PMID 37062296 (retracted; notice online 2023-12-12), cited in
  AAO2024ARHL-KAS02/-KAS06; parent ruling P2-5 (see below). Plus 1
  EoC-flagged attachment, NOT a zombie by definition: PMID 11087881 (VIGOR,
  EoC 2005) in AAO2021OPI-KAS06.

## Verification performed (Phase 2)

- B1-style independent recounts for all 15 prior documents: AAO 124/124 items
  exact (from the producers' span sets); ICAR fresh-parse recount 102/102
  exact; EPOS reproduction recount from source PDFs (totals exact; 148/150
  item sets identical, one disputed citation resolved as ruling P2-1).
- Pivotal-screen content check caught a producer section-mapping slip that
  count-based recounts cannot see (ruling P2-4).
- 10% re-classification sample (307 studies): initial disagreement 18.6%,
  traced to the main run's asymmetric title matching (database title glued
  with journal tails in printed citations); all 57 disagreements adjudicated
  in writing (`reclass_adjudication.csv`); the full affected stratum (824
  rows) was re-run under symmetric containment; adjudicated finals reproduced
  44/45 exactly (the one difference is a written F2 substance override,
  applied at merge as ruling P2-2). NO Kaggle B2 pass in Phase 2 — a
  deliberate scope difference from L3, pre-specified in the addendum §4
  (Phase-2 outputs are rates over sets, not per-item pivotal headlines).

## Disclosures and limitations

1. AAO2007SIN-09 was admitted under Amendment v2.3 after a census omission
   was found during extraction; it is parent-adjudicated (verdict: dropped)
   and was NOT part of the Phase-1 blind sample, which predates it.
2. ARIA 2020 has no item-level citation apparatus; per addendum §2 it is
   excluded from all pooled Phase-2 rates and reported separately.
3. Adjudication rulings of record: P2-1 (EPOS 2007 ref 789 reassigned
   EPOS2007-29 → EPOS2007-09 on verbatim text); P2-2 (tosm 1982 design
   'other' by F2 substance override); P2-3 (mandelem 1992 RCT stands);
   P2-4 (EPOS2012-84 attachment set corrected to §5.7.7.3 refs 1629/1630/1631;
   pivotal re-screened by the parent); P2-5 (PMID 37062296 zombie confirmed —
   the citing guideline's own reference list already prints the citation with
   a 'RETRACTED:' prefix).
4. Identity coverage: prior attachments 88.8% PMID-identified; current side
   60.0% of reference instances PMID-identified, the rest matched on parsed
   titles (title parsing validated at 84.4% strict agreement; parse error can
   only split identities, so turnover for the parse-heavy documents
   ICAR2023AR and AAO2019SHL may be biased slightly upward).
5. Residual unresolvables, recorded never guessed: 25 current-version
   pivotals without a resolvable PMID (excluded from persistence
   denominators); 44 title-only persistent identities not screenable for
   retraction status; 1 study unfetched after full retries (wongdl 1988);
   4 parse-broken SIN09 citations unverified; 386 unverified prior-side
   studies (no design class; skipped in pivotal selection).
6. EPOS 2020 rewrote every statement as prose evidence summaries (T12:
   0 identical / 79 modified / 9 dropped) — zero verbatim survival there is a
   structural property of that rewrite, not reviewer disagreement.

## Headline reading

Recommendations themselves are highly stable across versions (92.1% survive;
2.6% flip direction), but their evidence base is not: two-thirds of a new
version's citations are new, and four-fifths of carried recommendations rest
on a different pivotal study than the version before. Zombie citations are
rare but real, and concentrated where it matters most — three of them are the
pivotal study of a current recommendation.

## Amendment v2.5 addendum (2026-11-08) — L3 re-freeze downstream

The L3 dataset was re-frozen under Amendment v2.5 (sha256 2785235d…).
L5's frozen data files are unchanged; two reported values are superseded:
- **Pivotal persistence: 60/292 = 20.5%** (frozen: 57/292 = 19.5%),
  transition-cluster bootstrap 95% CI [0.154, 0.285]. The frozen
  construction was first replicated verbatim (57/292 and the v2.4 S1
  interval reproduced exactly) before the re-frozen current-side
  pivotals were substituted; five pairs flipped status (four
  different→same, one same→different). Turnover measures do not depend
  on pivotals and are unchanged (the v2.4 S2 range presentation stands).
- **Zombie pivotals, stratum (b): 2** (frozen: 3) over 588 screened
  unique PMIDs. EPOS2020-16's determination is withdrawn — EPOS cites
  the 2011 zinc record (PMID 21328251), never withdrawn; the withdrawn
  2015 update is not cited. Standing zombies: AAO2025SIN2-KAS12
  (PMID 30184244) and EPOS2020-69 (PMID 27110699), both re-verified
  withdrawn on 2026-11-08. All 22 pivotals changed by v2.5 were
  re-screened: 22/22 live.
Detail: l3_production/remediation_v25/downstream/downstream_report.md.
