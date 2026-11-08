#!/usr/bin/env python3
"""Build data/changes.json — the "What changed" page data — from the frozen
Layer-5 alignment and the frozen L1/L2 dataset.

No statistic is hand-typed: verdict counts, direction flips, survival and the
evidence-tier / strength movement summary are all computed here from
analysis/frozen_l5/phase1_alignment_final.csv joined to
analysis/frozen_dataset_l1l2.csv (plus the Amendment v2.3 added item,
analysis/frozen_l5/l5_added_item_v23.csv, which lives outside the frozen
L1/L2 census file). The computed headlines are ASSERTED against the frozen
values stated in analysis/frozen_l5/L5_freeze_report.md:

  - alignment rulings 394 = identical 130 / modified 231 / dropped 33
  - pooled survival excl. ARIA (T15): 359/390 = 92.1%
  - direction flips among both-stanced carried pairs excl. ARIA: 7/267
  - evidence tier (U): up 58 / down 18 / same 246 (n = 322, all carried pairs
    whose two sides both carry a mappable grade)
  - strength (S): strengthened 33 / weakened 4 / same 179 (n = 216, carried
    pairs whose two sides both map into S/M/W)
  - ARIA T15 kept separate throughout: 4 rulings, 2 carried, 2 dropped

The U/S mapping functions are copied verbatim from tools/build_data.py
(Codebook v0.1 §4 mapping, from the frozen analysis/l1l2_compute.py).

Run:  python3 site/tools/build_changes.py
Output: site/data/changes.json
"""
import csv, json, os, re
from collections import Counter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SITE = os.path.join(ROOT, 'site')
A = os.path.join(ROOT, 'analysis')

def rd(path):
    with open(path, newline='', encoding='utf-8') as fh:
        return list(csv.DictReader(fh))

def doc_of(rec_id):
    return rec_id.rsplit('-', 1)[0]

def parse_key(rec_id):
    """Frozen L1/L2 <-> L3 join key (same rule as tools/build_data.py)."""
    doc, suf = rec_id.rsplit('-', 1)
    if suf.startswith('KAS'):
        suf = suf[3:]
    num = ''
    while suf and suf[0].isdigit():
        num += suf[0]; suf = suf[1:]
    return (doc, (int(num) if num else 0, suf.upper()))

# --- U/S mapping, verbatim from tools/build_data.py -------------------------
_UNRATED = ('', 'none', 'N/A', 'Uncertain', 'Not applicable', 'Unable to determine', 'Grade X')
def _map_grade(g):
    g = (g or '').strip()
    if g in _UNRATED or g.startswith('no data'): return None
    m = re.match(r'(?:Grade\s+)?([ABCD])\b', g)
    if m: return {'A': 'U1', 'B': 'U2', 'C': 'U3', 'D': 'U4'}[m.group(1)]
    low = g.lower()
    if low == 'high': return 'U1'
    if low == 'moderate': return 'U2'
    if low == 'low': return 'U3'
    if low == 'very low': return 'U4'
    m = re.match(r'(I{1,3}|IV)(a|b)?\b', g)
    if m: return {'I': 'U1', 'II': 'U2', 'III': 'U3', 'IV': 'U4'}[m.group(1)]
    m = re.match(r'([1-5])(a|b)?\b', g)
    if m: return {'1': 'U1', '2': 'U2', '3': 'U3', '4': 'U4', '5': 'U4'}[m.group(1)]
    return 'UNMAPPED:' + g
def _map_strength(s):
    s = (s or '').strip()
    if s in ('Strong recommendation', 'Strong recommendation against'): return 'S'
    if s in ('Recommendation', 'Recommendation against', 'Recommendation (against)',
             'Moderate recommendation', 'Negative recommendation',
             'Moderate-to-strong recommendation'): return 'M'
    if s in ('Option', 'Conditional recommendation', 'Weak recommendation', 'Opinion'): return 'W'
    if s in ('No recommendation', 'No consensus', 'No indication', ''): return 'NONE'
    return 'UNMAPPED:' + s

# --------------------------------------------------------------------- load
l12 = rd(os.path.join(A, 'frozen_dataset_l1l2.csv'))
added = rd(os.path.join(A, 'frozen_l5', 'l5_added_item_v23.csv'))
by_rec = {r['rec_id']: r for r in l12 + added}
align = rd(os.path.join(A, 'frozen_l5', 'phase1_alignment_final.csv'))
items = json.load(open(os.path.join(SITE, 'data', 'items.json')))
site_by_key = {parse_key(i['rec']): i for i in items}

docmeta = {}
for r in l12 + added:
    d = doc_of(r['rec_id'])
    if d not in docmeta:
        docmeta[d] = {'guideline': r['guideline'], 'society': r['society'],
                      'year': int(r['year'])}

# frozen-file hashes for provenance (read, never typed)
hashes = {}
with open(os.path.join(A, 'frozen_l5', 'freeze_sha256.txt')) as fh:
    for line in fh:
        parts = line.split()
        if len(parts) == 2:
            hashes[parts[1].lstrip('*')] = parts[0]

STANCED = ('for', 'against')
ARIA_T = 'T15'

def side(rec_id):
    r = by_rec[rec_id]
    d = doc_of(rec_id)
    return {'rec': rec_id, 'doc': d, 'name': docmeta[d]['guideline'],
            'year': docmeta[d]['year'], 'statement': r['statement_text'],
            'direction': r['direction'], 'tier': r['strength_raw'],
            'grade': r['grade_raw']}

# ------------------------------------------------------------------ compute
verdicts = Counter(r['verdict'] for r in align)
assert len(align) == 394, len(align)
assert verdicts == {'carried-identical': 130, 'carried-modified': 231, 'dropped': 33}, verdicts
for r in align:
    assert r['prior_rec'] in by_rec, r['prior_rec']
    if r['verdict'] != 'dropped':
        assert r['current_rec'] in by_rec, r['current_rec']

flips, dropped, aria_flips, aria_dropped = [], [], [], []
carried = [r for r in align if r['verdict'] != 'dropped']
both_stanced_pooled = 0
for r in align:
    p = by_rec[r['prior_rec']]
    if r['verdict'] == 'dropped':
        e = {'transition': r['transition'], 'family': docmeta[doc_of(r['prior_rec'])]['guideline'],
             'prior_doc': doc_of(r['prior_rec']), 'current_doc': None,
             'prior_name': docmeta[doc_of(r['prior_rec'])]['guideline'],
             'prior_year': docmeta[doc_of(r['prior_rec'])]['year'],
             'prior_rec': r['prior_rec'], 'prior_statement': p['statement_text'],
             'prior_direction': p['direction'], 'prior_tier': p['strength_raw'],
             'prior_grade': p['grade_raw'], 'basis': r['basis']}
        (aria_dropped if r['transition'] == ARIA_T else dropped).append(e)
        continue
    c = by_rec[r['current_rec']]
    if p['direction'] in STANCED and c['direction'] in STANCED:
        if r['transition'] != ARIA_T:
            both_stanced_pooled += 1
        if p['direction'] != c['direction']:
            ps, cs = side(r['prior_rec']), side(r['current_rec'])
            site_rec = site_by_key.get(parse_key(r['current_rec']))
            e = {'transition': r['transition'], 'family': ps['name'],
                 'prior_doc': ps['doc'], 'current_doc': cs['doc'],
                 'prior_name': ps['name'], 'current_name': cs['name'],
                 'prior_year': ps['year'], 'current_year': cs['year'],
                 'prior_rec': ps['rec'], 'prior_statement': ps['statement'],
                 'prior_direction': ps['direction'], 'prior_tier': ps['tier'],
                 'prior_grade': ps['grade'],
                 'current_rec': cs['rec'], 'current_statement': cs['statement'],
                 'current_direction': cs['direction'], 'current_tier': cs['tier'],
                 'current_grade': cs['grade'],
                 'current_rec_site': site_rec['rec'] if site_rec else None,
                 'basis': r['basis']}
            (aria_flips if r['transition'] == ARIA_T else flips).append(e)

pooled = [r for r in align if r['transition'] != ARIA_T]
carried_pooled = sum(1 for r in pooled if r['verdict'] != 'dropped')
assert len(pooled) == 390 and carried_pooled == 359, (len(pooled), carried_pooled)
assert both_stanced_pooled == 267, both_stanced_pooled
assert len(flips) == 7, len(flips)
assert len(dropped) == 31 and len(aria_dropped) == 2 and len(dropped) + len(aria_dropped) == 33
aria_rows = [r for r in align if r['transition'] == ARIA_T]
assert len(aria_rows) == 4 and sum(1 for r in aria_rows if r['verdict'] != 'dropped') == 2
assert len(aria_flips) == 0

# direction agreement between the L1/L2 join and the published items.json
joined_dir_ok = 0
for r in carried:
    it = site_by_key.get(parse_key(r['current_rec']))
    if it:
        assert it['direction'] == by_rec[r['current_rec']]['direction'], r['current_rec']
        joined_dir_ok += 1
print('current-side direction agreement with items.json:', joined_dir_ok, 'joined pairs')

# tier / strength movement over carried pairs (frozen-report populations)
UORD = {'U1': 1, 'U2': 2, 'U3': 3, 'U4': 4}
SORD = {'S': 3, 'M': 2, 'W': 1}
u_up = u_down = u_same = 0
s_str = s_weak = s_same = 0
for r in carried:
    p, c = by_rec[r['prior_rec']], by_rec[r['current_rec']]
    pu, cu = _map_grade(p['grade_raw']), _map_grade(c['grade_raw'])
    if pu in UORD and cu in UORD:
        if UORD[cu] < UORD[pu]: u_up += 1
        elif UORD[cu] > UORD[pu]: u_down += 1
        else: u_same += 1
    ps, cs = _map_strength(p['strength_raw']), _map_strength(c['strength_raw'])
    if ps in SORD and cs in SORD:
        if SORD[cs] > SORD[ps]: s_str += 1
        elif SORD[cs] < SORD[ps]: s_weak += 1
        else: s_same += 1
tier_summary = {
    'U': {'up': u_up, 'down': u_down, 'same': u_same, 'n': u_up + u_down + u_same},
    'S': {'strengthened': s_str, 'weakened': s_weak, 'same': s_same,
          'n': s_str + s_weak + s_same},
    'basis': 'Computed here from the frozen L1/L2 grade_raw / strength_raw fields '
             'joined through the frozen L5 alignment (U over carried pairs where '
             'both sides map to a U grade; S over carried pairs where both sides '
             'map into S/M/W). Asserted equal to L5_freeze_report.md Phase 1.',
}
assert tier_summary['U'] == {'up': 58, 'down': 18, 'same': 246, 'n': 322}, tier_summary['U']
assert tier_summary['S'] == {'strengthened': 33, 'weakened': 4, 'same': 179, 'n': 216}, tier_summary['S']

flips.sort(key=lambda e: (e['transition'], e['prior_rec']))
dropped.sort(key=lambda e: (e['transition'], e['prior_rec']))
aria_dropped.sort(key=lambda e: e['prior_rec'])

out = {
    'flips': flips,
    'dropped': dropped,
    'tier_summary': tier_summary,
    'aria': {'flips': aria_flips, 'dropped': aria_dropped,
             'totals': {'rulings': len(aria_rows), 'carried': 2, 'dropped': 2}},
    'totals': {'rulings': len(align), 'identical': verdicts['carried-identical'],
               'modified': verdicts['carried-modified'], 'dropped': verdicts['dropped'],
               'dropped_pooled': len(dropped), 'flips': len(flips),
               'flips_den': both_stanced_pooled,
               'survival_num': carried_pooled, 'survival_den': len(pooled),
               'survival_pct': round(100.0 * carried_pooled / len(pooled), 1)},
    'source': 'Generated by site/tools/build_changes.py from '
              'analysis/frozen_l5/phase1_alignment_final.csv + '
              'analysis/frozen_dataset_l1l2.csv + analysis/frozen_l5/l5_added_item_v23.csv; '
              'headlines asserted against analysis/frozen_l5/L5_freeze_report.md.',
    'provenance_sha256': {'phase1_alignment_final.csv': hashes.get('phase1_alignment_final.csv'),
                          'L5_freeze_report.md': hashes.get('L5_freeze_report.md')},
}
with open(os.path.join(SITE, 'data', 'changes.json'), 'w', encoding='utf-8') as fh:
    json.dump(out, fh, ensure_ascii=False, separators=(',', ':'))
print('wrote data/changes.json | flips', len(flips), '| dropped pooled', len(dropped),
      '| ARIA dropped', len(aria_dropped), '| U', tier_summary['U'], '| S', tier_summary['S'])
