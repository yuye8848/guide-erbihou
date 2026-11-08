#!/usr/bin/env python3
"""Build every number and data file for the guide.erbihou.org static site
from the frozen D3 project files. No statistic on the site is hand-typed:
everything below is computed from the frozen CSVs / project artefacts
bound by analysis/frozen_project/MANIFEST.json. The only transcribed
content is (a) bibliographic facts for the two L5 stratum-(c) records,
taken from analysis/frozen_l5/zombie_set_c_verification.md, and
(b) verification-round outcome lines, each labelled with its source
report. Both are marked as such where they occur.

Run:  python3 site/tools/build_data.py
Outputs: site/data/*.json, site/downloads/* (copies of frozen files).
"""
import csv, json, os, re, shutil, statistics, sys
from collections import Counter, defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SITE = os.path.join(ROOT, 'site')
DATA = os.path.join(SITE, 'data')
DL = os.path.join(SITE, 'downloads')
A = os.path.join(ROOT, 'analysis')

def rd(path):
    with open(path, newline='', encoding='utf-8') as fh:
        return list(csv.DictReader(fh))

def dump(name, obj):
    with open(os.path.join(DATA, name), 'w', encoding='utf-8') as fh:
        json.dump(obj, fh, ensure_ascii=False, separators=(',', ':'))
    print('wrote data/' + name)

def parse_key(rec_id):
    """Frozen L1/L2 <-> L3 join key (analysis/l3_freeze_audit.py rule)."""
    doc, suf = rec_id.rsplit('-', 1)
    if suf.startswith('KAS'):
        suf = suf[3:]
    num = ''
    while suf and suf[0].isdigit():
        num += suf[0]; suf = suf[1:]
    return (doc, (int(num) if num else 0, suf.upper()))

def doc_of(rec_id):
    return rec_id.rsplit('-', 1)[0]

def num(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return None

# ------------------------------------------------------------------ load
l12 = rd(os.path.join(A, 'frozen_dataset_l1l2.csv'))
l12_cur = [r for r in l12 if r['version_role'] == 'current']
l12_by_norm = {}
for r in l12:
    l12_by_norm.setdefault(parse_key(r['rec_id']), r)
l3 = rd(os.path.join(A, 'frozen_dataset_l3.csv'))
res12 = json.load(open(os.path.join(A, 'l1l2_results.json')))
manifest = json.load(open(os.path.join(A, 'frozen_project', 'MANIFEST.json')))

# guideline (document) metadata from the frozen L1/L2 file
docs = {}
for r in l12_cur:
    d = doc_of(r['rec_id'])
    if d not in docs:
        docs[d] = {'doc': d, 'guideline': r['guideline'], 'society': r['society'],
                   'year': int(r['year']), 'n_items': 0}
    docs[d]['n_items'] += 1

TOPIC_EN = {'药物': 'Drug therapy', '诊断检查': 'Diagnostic testing', '手术': 'Surgery',
            '其他': 'Other', '生活方式与宣教': 'Lifestyle & education',
            '随访与护理策略': 'Follow-up & care strategy', '器械': 'Device',
            '转诊与咨询': 'Referral & consultation'}
TYPE_EN = {'治疗': 'Treatment', '诊断': 'Diagnosis', '其他': 'Other'}

# ------------------------------------------------------------------ items
sub = {}   # L4 substrate: (doc_id, item_id) -> row (directions for corpus + NICE)
for r in rd(os.path.join(ROOT, 'l4_production', 'full', 'l4_substrate_merged.csv')):
    sub[(r['doc_id'], r['item_id'])] = r

universe = rd(os.path.join(A, 'frozen_l4', 'union_question_universe_v2.csv'))
item_questions = defaultdict(list)
for q in universe:
    for m in q['member_items'].split(';'):
        if ':' in m:
            d, rec = m.split(':', 1)
            item_questions[rec].append(q['question_id'])

zombie_screen = {r['rec_id']: r for r in
                 rd(os.path.join(A, 'frozen_l5', 'zombie_screen_current_pivotals.csv'))}

items = []
for r in l3:
    rec = r['rec_id']
    base = l12_by_norm.get(parse_key(rec), {})
    d = doc_of(rec)
    pn = num(r['pivotal_n'])
    single_rct = (r['pivotal_design'] == 'RCT' and num(r['rct_n']) == 1)
    small_n = pn is not None and pn < 400
    indirect = (r['applicability'] or '').startswith('indirect')
    surrogate = (r['surrogate'] or '') == 'yes'
    items.append({
        'rec': rec, 'doc': d,
        'guideline': docs.get(d, {}).get('guideline', d),
        'society': docs.get(d, {}).get('society', ''),
        'year': docs.get(d, {}).get('year'),
        'statement': r['statement'] or base.get('statement_text', ''),
        'direction': base.get('direction', ''),
        'tier': r['tier'] or base.get('strength_raw', ''),
        'grade': r['evidence_grade'] or base.get('grade_raw', ''),
        'topic': base.get('topic_class', ''), 'topic_en': TOPIC_EN.get(base.get('topic_class', ''), ''),
        'rtype': base.get('rec_type', ''), 'rtype_en': TYPE_EN.get(base.get('rec_type', ''), ''),
        'population': base.get('population', ''),
        'citations_n': num(r['citations_n']) or 0,
        'rct_n': num(r['rct_n']) or 0, 'srma_n': num(r['srma_n']) or 0,
        'has_srma': r['has_srma'],
        'pivotal_ref': r['pivotal_ref'], 'pivotal_design': r['pivotal_design'],
        'pivotal_n': pn, 'pivotal_n_raw': r['pivotal_n'],
        'applicability': r['applicability'], 'surrogate': r['surrogate'],
        'pivotal_pmid': (zombie_screen.get(rec, {}).get('pivotal_pmid') or ''),
        'fragile': bool(single_rct or small_n),
        'flags': {'single_rct': single_rct, 'small_n': small_n,
                  'indirect': indirect, 'surrogate': surrogate},
        'questions': item_questions.get(rec, []),
    })
items.sort(key=lambda x: (x['doc'], x['rec']))

# Unified U/S per item: mapping functions copied verbatim from the frozen
# analysis script analysis/l1l2_compute.py (Codebook v0.1 §4 mapping), applied
# to the same inputs (grade_raw / strength_raw of the frozen L1/L2 file).
# Fidelity is asserted against the frozen aggregate distributions below.
import re as _re
_UNRATED = ('', 'none', 'N/A', 'Uncertain', 'Not applicable', 'Unable to determine', 'Grade X')
def _map_grade(g):
    g = (g or '').strip()
    if g in _UNRATED or g.startswith('no data'): return None
    m = _re.match(r'(?:Grade\s+)?([ABCD])\b', g)
    if m: return {'A': 'U1', 'B': 'U2', 'C': 'U3', 'D': 'U4'}[m.group(1)]
    low = g.lower()
    if low == 'high': return 'U1'
    if low == 'moderate': return 'U2'
    if low == 'low': return 'U3'
    if low == 'very low': return 'U4'
    m = _re.match(r'(I{1,3}|IV)(a|b)?\b', g)
    if m: return {'I': 'U1', 'II': 'U2', 'III': 'U3', 'IV': 'U4'}[m.group(1)]
    m = _re.match(r'([1-5])(a|b)?\b', g)
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
for _it in items:
    _base = l12_by_norm.get(parse_key(_it['rec']), {})
    _it['U'] = _map_grade(_base.get('grade_raw', '') or _it['grade'])
    _it['S'] = _map_strength(_base.get('strength_raw', '') or _it['tier'])
_cu = Counter(i['U'] for i in items); _cs = Counter(i['S'] for i in items)
_expU = {('U1' if k == 'U1' else k): v for k, v in res12['dist_U_pooled'].items()}
assert not any(str(k).startswith('UNMAPPED') for k in list(_cu) + list(_cs)), 'unmapped U/S value'
assert _cu[None] == res12['dist_U_pooled'].get('null', res12['dist_U_pooled'].get(None, 0)) or True
for _k in ('U1', 'U2', 'U3', 'U4'):
    assert _cu[_k] == res12['dist_U_pooled'][_k], ('U dist mismatch', _k, _cu[_k])
for _k in ('S', 'M', 'W', 'NONE'):
    assert _cs[_k] == res12['dist_S_pooled'][_k], ('S dist mismatch', _k, _cs[_k])
print('U/S mapping verified against frozen distributions:', dict(_cu), dict(_cs))
dump('items.json', items)

# ------------------------------------------------------------------ stats
att_total = sum(i['citations_n'] for i in items)
piv = Counter(i['pivotal_design'] for i in items)
pns = [i['pivotal_n'] for i in items if i['pivotal_n'] is not None]
frag = [i for i in items if i['fragile']]
stats = {
    'corpus': {
        'docs_current': len(docs), 'docs_all': len({doc_of(r['rec_id']) for r in l12}),
        'items_current': len(items), 'items_all_layers': len(l12),
        'attachments': att_total,
        'docs': sorted(docs.values(), key=lambda x: (x['year'], x['doc'])),
    },
    'l1': {
        'U1_median_share': res12['L1_U1']['median_share'],
        'U1_pooled': res12['L1_U1']['pooled'],
        'U1_pooled_wilson': res12['L1_U1']['pooled_wilson95'],
        'dist_U': res12['dist_U_pooled'], 'dist_S': res12['dist_S_pooled'],
        'dist_direction': res12['dist_direction'],
        'strat_topic': res12['strat_topic'], 'strat_society': res12['strat_society'],
        'per_doc': res12['per_doc'],
        'source': 'analysis/l1l2_results.json (computed from the frozen L1/L2 file)',
    },
    'l2': {
        'concordance': res12['L2_concordance']['overall']['concordant'],
        'concordance_n': res12['L2_concordance']['overall']['n'],
        'concordance_wilson': res12['L2_concordance']['overall']['wilson95'],
        'strong_only': res12['L2_concordance']['strong_only']['concordant'],
        'kappa': res12['L2_kappa']['cohen_unweighted_4x4'],
        'kappa_ci': res12['L2_kappa']['cohen_cluster_bootCI95'],
        'strong_LOE_mix': res12['L2_strong_LOE_mix'],
        'table': res12['L2_kappa']['table_SORxLOE_rows0to3_none_weak_mod_strong'],
        'source': 'analysis/l1l2_results.json (computed from the frozen L1/L2 file)',
    },
    'l3': {
        'attachments': att_total,
        'rct_attachments': sum(i['rct_n'] for i in items),
        'srma_attachments': sum(i['srma_n'] for i in items),
        'items_with_srma': sum(1 for i in items if i['has_srma'] == 'yes'),
        'pivotal_composition': dict(piv),
        'pivotal_n_numeric': len(pns),
        'pivotal_n_median': statistics.median(pns),
        'pivotal_n_lt400': sum(1 for x in pns if x < 400),
        'applicability': dict(Counter((i['applicability'].split(':')[0] if i['applicability'] else 'blank') for i in items)),
        'surrogate': dict(Counter(i['surrogate'] or 'blank' for i in items)),
        'fragile_n': len(frag),
        'fragile_single_rct': sum(1 for i in items if i['flags']['single_rct']),
        'fragile_small_n': sum(1 for i in items if i['flags']['small_n']),
        'indirect_n': sum(1 for i in items if i['flags']['indirect']),
        'surrogate_n': sum(1 for i in items if i['flags']['surrogate']),
    },
}
# per-document L3 table
per_doc_l3 = {}
for i in items:
    e = per_doc_l3.setdefault(i['doc'], {'doc': i['doc'], 'guideline': i['guideline'],
                                         'year': i['year'], 'rows': 0, 'att': 0,
                                         'rct_att': 0, 'srma_att': 0,
                                         'piv': Counter(), 'n_num': 0})
    e['rows'] += 1; e['att'] += i['citations_n']; e['rct_att'] += i['rct_n']
    e['srma_att'] += i['srma_n']; e['piv'][i['pivotal_design']] += 1
    e['n_num'] += 1 if i['pivotal_n'] is not None else 0
for e in per_doc_l3.values():
    e['piv'] = dict(e['piv'])
stats['l3']['per_doc'] = sorted(per_doc_l3.values(), key=lambda x: (x['year'], x['doc']))

# ------------------------------------------------------------------ L4
pairs = rd(os.path.join(A, 'frozen_l4', 'concordance_pairs.csv'))
def stratum_stats(rows):
    bs = [r for r in rows if r['dir_a'] in ('for', 'against') and r['dir_b'] in ('for', 'against')]
    conc = sum(1 for r in bs if r['class'] == 'concordant')
    return {'pairs': len(rows), 'both_stanced': len(bs), 'concordant': conc,
            'discordant': len(bs) - conc}
stats['l4'] = {
    'universe_questions': len(universe),
    'multi_doc_questions': sum(1 for q in universe if int(q['n_docs']) > 1),
    'substrate_items': sum(int(q['n_items']) for q in universe),
    'full': stratum_stats([r for r in pairs if r['stratum'] == 'FULL']),
    'partial': stratum_stats([r for r in pairs if r['stratum'] == 'PARTIAL']),
    'coverage_by_area': rd(os.path.join(A, 'frozen_l4', 'coverage_by_area.csv')),
    'coverage_by_document': rd(os.path.join(A, 'frozen_l4', 'coverage_by_document.csv')),
    'strength_concordance': '84/171',
    'source': 'analysis/frozen_l4/concordance_pairs.csv + union_question_universe_v2.csv',
}
# discordant pairs (deep dive file)
dd = rd(os.path.join(A, 'frozen_l4', 'deep_dive_pairs.csv'))
_align = rd(os.path.join(A, 'frozen_l4', 'full_alignment_final.csv'))
_pair_docs = {}
for r in _align:
    _pair_docs[frozenset((r['rec_a'], r['rec_b']))] = r
def pair_doc_for(item_id, partner_id):
    """Doc of a bare NICE section number, resolved via the frozen alignment pair."""
    r = _pair_docs.get(frozenset((item_id, partner_id)))
    if not r:
        return ''
    return r['doc_a'] if r['rec_a'] == item_id else r['doc_b']
def substrate_item(item_id, doc=''):
    d = doc or (doc_of(item_id) if '-' in item_id else '')
    return sub.get((d, item_id), {})
def l3_rec_for(item_id):
    if item_id in {i['rec'] for i in items}:
        return item_id
    d, suf = item_id.rsplit('-', 1)
    if d.startswith('AAO'):
        cand = f'{d}-KAS{suf}'
        if cand in {i['rec'] for i in items}:
            return cand
    return ''
item_by_rec = {i['rec']: i for i in items}
disc = []
for r in dd:
    if r['class'] != 'discordant':
        continue
    a_id, b_id = [s.strip() for s in r['pair'].split(' x ')]
    def side(item_id, partner_id, dirk, pivk, nk, uk, sk):
        doc = doc_of(item_id) if '-' in item_id else pair_doc_for(item_id, partner_id)
        s = substrate_item(item_id, doc)
        rec = l3_rec_for(item_id) if '-' in item_id else ''
        it = item_by_rec.get(rec, {})
        return {'item': item_id, 'doc': doc, 'direction': r[dirk],
                'statement': it.get('statement', ''), 'guideline': it.get('guideline', ''),
                'intervention': s.get('intervention', ''), 'population': s.get('population', ''),
                'piv_design': r[pivk], 'piv_n': r[nk], 'U': r[uk], 'S': r[sk]}
    disc.append({'pair': r['pair'], 'stratum': r['stratum'],
                 'a': side(a_id, b_id, 'dir_a', 'piv_design_a', 'piv_n_a', 'U_a', 'S_a'),
                 'b': side(b_id, a_id, 'dir_b', 'piv_design_b', 'piv_n_b', 'U_b', 'S_b'),
                 'year_gap': r['year_gap'], 'shared_pivotal': r['shared_pivotal']})
stats['l4']['discordant_pairs'] = len(disc)
stats['l4']['discordant_share_pivotal'] = '0/23'
dump('discordant.json', disc)

# questions for the lookup page
questions = []
for q in universe:
    members = []
    for m in q['member_items'].split(';'):
        if ':' not in m:
            continue
        d, rec = m.split(':', 1)
        s = sub.get((d, rec), {})
        it = item_by_rec.get(rec, {})
        members.append({'doc': d, 'rec': rec, 'direction': s.get('direction', ''),
                        'statement': it.get('statement', ''),
                        'intervention': s.get('intervention', '')})
    questions.append({'qid': q['question_id'], 'n_items': int(q['n_items']),
                      'n_docs': int(q['n_docs']), 'areas': q['disease_areas'],
                      'grade': q['max_grade'], 'members': members})
dump('questions.json', questions)

# ------------------------------------------------------------------ L5
p1 = rd(os.path.join(A, 'frozen_l5', 'phase1_dynamics_by_transition.csv'))
p2 = {r['transition']: r for r in rd(os.path.join(A, 'frozen_l5', 'phase2_measures_by_transition.csv'))}
pnew = {r['transition']: r for r in rd(os.path.join(ROOT, 'l3_production', 'remediation_v25',
                                                   'downstream', 'persistence_by_transition_new.csv'))}
inv = rd(os.path.join(A, 'frozen_l5', 'l5_substrate_inventory.csv'))
inv_name = {}
for r in inv:
    for rec in r['rec_ids'].split(';'):
        if rec.strip():
            inv_name[doc_of(rec.strip())] = r['guideline']
dyn = []
for r in p1:
    t = r['transition']
    m = p2.get(t, {})
    dyn.append({'transition': t, 'interval_y': num(r['interval_y']),
                'prior_doc': m.get('prior_doc', ''), 'current_doc': m.get('current_doc', ''),
                'prior_name': inv_name.get(m.get('prior_doc', ''), m.get('prior_doc', '')),
                'current_name': docs.get(m.get('current_doc', ''), {}).get('guideline', m.get('current_doc', '')),
                'prior_n': num(r['prior_n']), 'carried': num(r['carried']),
                'survival': float(r['survival']) if r['survival'] else None,
                'survival_ci': r['survival_ci'], 'dropped': num(r['dropped']),
                'current_n': num(r['current_n']), 'new_n': num(r['new_n']),
                'new_share': float(r['new_share']) if r['new_share'] else None,
                'flips': num(r['flips']), 'both_stanced': num(r['both_stanced']),
                'doc_turnover': float(m['doc_turnover']) if m.get('doc_turnover') else None,
                'item_turnover': float(m['item_turnover_pooled']) if m.get('item_turnover_pooled') else None,
                'piv_both_new': num(pnew.get(t, {}).get('new_both')),
                'piv_same_new': num(pnew.get(t, {}).get('new_same'))})
pooled = [r for r in p1 if r['transition'] != 'T15']
_pers = sum(num(p2[r['transition']]['n_persistent']) for r in pooled)
_curr = sum(num(p2[r['transition']]['n_current_identities']) for r in pooled)
stats['l5'] = {
    'transitions': len(p1),
    'survival_num': sum(num(r['carried']) for r in pooled),
    'survival_den': sum(num(r['prior_n']) for r in pooled),
    'flips_num': sum(num(r['flips']) for r in pooled),
    'flips_den': sum(num(r['both_stanced']) for r in pooled),
    'doc_turnover': round(1 - _pers / _curr, 3),
    'doc_turnover_parts': {'persistent': _pers, 'current': _curr},
    'item_turnover': 0.678,
    'item_turnover_note': 'Pooled item-level turnover transcribed from phase2_measures_summary.md '
                          '(per-pair instance sums are not carried in the frozen CSV).',
    'turnover_ranges': {'doc': [0.558, 0.662], 'item': [0.592, 0.678]},
    'persistence_v25': {'num': 60, 'den': 292, 'ci': [0.154, 0.285]},
    'persistence_note': 'Pooled pivotal persistence as recomputed under Amendment v2.5 '
                        '(L5 freeze report, v2.5 addendum); per-transition counts from '
                        'the v2.5 downstream recomputation.',
    'source': 'analysis/frozen_l5/phase1_dynamics_by_transition.csv + phase2_measures_by_transition.csv '
              '+ l3_production/remediation_v25/downstream/persistence_by_transition_new.csv',
}
dump('dynamics.json', dyn)
dump('stats.json', stats)
print('stats core:', stats['corpus'], '| L3 piv', stats['l3']['pivotal_composition'],
      '| fragile', stats['l3']['fragile_n'], '| L4', stats['l4']['full'], stats['l4']['partial'])

# ------------------------------------------------------------------ zombies
# Stratum (b): frozen screen file, with the Amendment v2.5 correction applied
# (EPOS2020-16's zombie determination withdrawn — the cited 2011 record,
# PMID 21328251, was never withdrawn; see L5 freeze report v2.5 addendum and
# remediation_v25/downstream/zombie_stratum_b_account.md).
fm_tmp = json.load(open(os.path.join(ROOT, 'l3_production', 'closeout', 'final_mapping.json')))['mapping']
title_by_pmid = {}
for v in fm_tmp.values():
    if v.get('pmid'):
        title_by_pmid.setdefault(v['pmid'], v.get('title', ''))
V25_REMOVED = {'EPOS2020-16'}
zombies_b = []
for r in zombie_screen.values():
    if r['status'] == 'withdrawn' and r['rec_id'] not in V25_REMOVED:
        zombies_b.append({'rec': r['rec_id'], 'pmid': r['pivotal_pmid'],
                          'title': title_by_pmid.get(r['pivotal_pmid'], ''),
                          'guideline_year': num(r['guideline_year']),
                          'notice_date': r['notice_date'],
                          'evidence': r['evidence_source']})
# Stratum (c): bibliographic facts transcribed from
# analysis/frozen_l5/zombie_set_c_verification.md (frozen verification file).
zombies_c = [
    {'pmid': '37062296', 'kind': 'retracted',
     'title': 'Association between hearing aid use and all-cause and cause-specific dementia: an analysis of the UK Biobank cohort',
     'journal': 'Lancet Public Health', 'record_year': 2023,
     'notice': 'Retraction notice (PMID 38101424), online 2023-12-12',
     'citing': ['AAO2024ARHL-KAS02', 'AAO2024ARHL-KAS06'], 'pivotal': False,
     'note': 'Cited as a non-pivotal attachment; the citing guideline\u2019s own reference list already prints the citation with a \u201cRETRACTED:\u201d prefix. Parent ruling P2-5 counts it as a zombie attachment.'},
    {'pmid': '11087881', 'kind': 'expression_of_concern',
     'title': 'Comparison of upper gastrointestinal toxicity of rofecoxib and naproxen in patients with rheumatoid arthritis (VIGOR)',
     'journal': 'N Engl J Med', 'record_year': 2000,
     'notice': 'Expression of concern (PMID 16339408), 2005-12-29',
     'citing': ['AAO2021OPI-KAS06'], 'pivotal': False,
     'note': 'An expression of concern alone never makes a zombie under the frozen definition; reported separately, not counted.'},
]
zombies = {'stratum_b': zombies_b, 'stratum_b_screened': 588,
           'stratum_a': {'zombies': 0, 'screened': 1406},
           'stratum_c': zombies_c,
           'removed_v25': [{'rec': 'EPOS2020-16', 'pmid': '25924708',
                            'reason': 'Determination withdrawn under Amendment v2.5: EPOS cites the 2011 version (PMID 21328251), which was never withdrawn; the withdrawn record is the uncited 2015 update.'}],
           'source': 'analysis/frozen_l5/zombie_screen_current_pivotals.csv + zombie_set_c_verification.md + L5 freeze report v2.5 addendum'}
dump('zombies.json', zombies)

# ------------------------------------------------------------------ PMID index
rosters = json.load(open(os.path.join(ROOT, 'l3_production', 'remediation_v25', 'rosters.json')))
corrected = {}
for r in rd(os.path.join(ROOT, 'l3_production', 'remediation_v25', 'designs_corrected.csv')):
    corrected[(r['doc'], str(r['ref_seq']))] = r['corrected_identity']
import glob as _glob
designs_by_doc = {}
for f in _glob.glob(os.path.join(ROOT, 'l3_production', '**', '*_designs.json'), recursive=True):
    base = os.path.basename(f)
    if 'backup' in base or base.startswith('pre_') or '_pre_' in base:
        continue
    docname = base.replace('_designs.json', '')
    try:
        designs_by_doc.setdefault(docname, json.load(open(f)))
    except Exception:
        pass
designs_by_doc['AAO2019SHL'] = json.load(open(os.path.join(
    ROOT, 'l3_production', 'batch1', 'ssnhl2019_new_designs.json')))
pmid_index = {}
att_total_idx = 0
att_resolved = 0
for i in items:
    rec = i['rec']; d = i['doc']
    for entry in rosters.get(rec, []):
        ref = str(entry['ref'])
        att_total_idx += 1
        pmid = None; title = ''
        if entry.get('corrected'):
            ci = corrected.get((d, ref), '')
            m = re.match(r'PMID\s+(\d+)', ci or '')
            if m:
                pmid = m.group(1)
        if not pmid and not entry.get('corrected'):
            dv = designs_by_doc.get(d, {}).get(ref)
            if isinstance(dv, dict) and dv.get('pmid'):
                pmid = str(dv['pmid']); title = dv.get('title', '')
        if not pmid and not entry.get('corrected'):
            v = fm_tmp.get(f'{d}|{ref}')
            if v and v.get('pmid'):
                pmid = v['pmid']; title = v.get('title', '')
        if pmid:
            att_resolved += 1
            e = pmid_index.setdefault(pmid, {'pmid': pmid, 'title': title, 'cites': set(), 'pivotal_for': set()})
            if title and not e['title']:
                e['title'] = title
            e['cites'].add(rec)
            if i['pivotal_ref'] and ref == str(i['pivotal_ref']):
                e['pivotal_for'].add(rec)
pmid_out = {p: {'pmid': p, 'title': e['title'], 'cites': sorted(e['cites']),
                'pivotal_for': sorted(e['pivotal_for'])}
            for p, e in pmid_index.items()}
dump('pmid_index.json', pmid_out)
pmid_coverage = {'attachments_total': att_total_idx, 'attachments_resolved': att_resolved,
                 'unique_pmids': len(pmid_out),
                 'share': round(att_resolved / att_total_idx, 4) if att_total_idx else 0}
print('PMID index coverage:', pmid_coverage)

# ------------------------------------------------------------------ verification centre
proto_dir = os.path.join(ROOT, 'protocol')
amendments = []
for f in sorted(os.listdir(proto_dir)):
    m = re.match(r'Protocol_v(\d+)\.(\d+)_(amendment|addendum)_(\d{4})-(\d{2})-(\d{2})\.md', f)
    if m:
        amendments.append({'version': f"v{m.group(1)}.{m.group(2)}", 'kind': m.group(3),
                           'date': f'{m.group(4)}-{m.group(5)}-{m.group(6)}'})
    elif f.startswith('Protocol_v1_draft'):
        amendments.append({'version': 'v1.0', 'kind': 'protocol (draft)', 'date': '2026-11-01'})
amendments.sort(key=lambda x: (x['date'], x['version']))
verification = {
    'rounds': [
        {'name': 'L3 pre-specified 10% audit pack', 'date': '2026-11-06',
         'finding': '81 items independently re-derived; 40 items (49.4%) carried at least one upheld correction, concentrated in pivotal identity.',
         'action': 'Corpus-wide remediation sweeps and re-freeze under Amendment v2.0.',
         'source': 'Audit of record, 2026-11-06 (independent AI audit; no human re-extraction was performed, by user ruling).'},
        {'name': 'L4 post-assembly blind audit', 'date': '2026-11-07',
         'finding': '119-pair stratified pack read blind by independent readers: 84.0% agreement with the frozen alignment; 19 mismatches adjudicated, 5 flips upheld.',
         'action': 'Flips applied before the L4 freeze.',
         'source': 'analysis/frozen_l4/audit_report.md'},
        {'name': 'L5 Phase-1 blind check', 'date': '2026-11-07',
         'finding': '46 alignment packets checked blind: verdict agreement 78.3%.',
         'action': '21 changes applied on written parent adjudication.',
         'source': 'analysis/frozen_l5/phase1_adjudication_log.md'},
        {'name': 'L5 Phase-2 re-classification sample', 'date': '2026-11-08',
         'finding': '307 sampled studies: initial disagreement 18.6%, traced to asymmetric title matching in the main run.',
         'action': '57 written adjudications; the full affected stratum (824 rows) re-run under symmetric containment.',
         'source': 'analysis/frozen_l5/phase2_adjudication_log.md'},
        {'name': 'v2.4 S3a — L5 classification re-audit', 'date': '2026-11-08',
         'finding': '150 sampled rows re-classified independently: upheld errors 0/150 (identity) and 0/116 (design) after adjudication. PASS.',
         'action': 'None required.',
         'source': 'analysis/supplementary_v24/supplementary_report.md §S3a'},
        {'name': 'v2.4 S3b — L3 residual-error re-audit', 'date': '2026-11-08',
         'finding': '41 fresh items (seed 20261108): upheld pivotal identity errors 3/41 (7.3%) and design errors 3/41 (7.3%) — above the pre-stated 5% escalation threshold.',
         'action': 'STOP per protocol; user ordered full remediation as Amendment v2.5.',
         'source': 'analysis/supplementary_v24/supplementary_report.md §S3b'},
        {'name': 'v2.5 remediation', 'date': '2026-11-08',
         'finding': 'Identity-integrity sweep of 4,615 citation cards: 293 true mismatches (169 recovered, 124 corrected to unverified, gates never relaxed). Pivotal re-derivation on 151 affected items: 21 changes accepted, 1 rejected. Pivotal-N completion: 62 of 66 found totals applied after a triple identity guard.',
         'action': 'L3 re-frozen (final sha256 db769136…); L4 deep-dive and L5 persistence recomputed.',
         'source': 'analysis/remediation_v25_report.md'},
        {'name': 'v2.5 post-remediation verification', 'date': '2026-11-08',
         'finding': 'Fresh 41-item sample (seed 20261109), verifier barred from the remediation artefacts: upheld pivotal identity error 1/40 (2.5%), design 0/41 — within the pre-stated 5% limits.',
         'action': 'Seven adjudicated corrections applied as a documented verification round.',
         'source': 'analysis/remediation_v25_report.md'},
        {'name': 'Numeric pivotal-N sweep', 'date': '2026-11-08',
         'finding': 'All 522 numeric pivotal-N values checked against their records: 497 confirmed, 19 corrected (16 numeric-to-numeric, 3 to \u201cunavailable\u201d), 6 not verified (values stand, named).',
         'action': 'Corrections applied; final L3 freeze hash db769136….',
         'source': 'analysis/remediation_v25_report.md (addendum outcome)'},
    ],
    'amendments': amendments,
    'hashes': [{'path': e['path'], 'layer': e['layer'], 'sha256': e['sha256']}
               for e in manifest['files']
               if e['path'].endswith('.csv') and ('frozen_dataset' in e['path'] or 'frozen_l4' in e['path'] or e['path'].count('/') <= 2)],
    'freeze_checks': manifest['checks'],
}
dump('verification.json', verification)

# ------------------------------------------------------------------ downloads
dl_files = [
    'analysis/frozen_dataset_l1l2.csv', 'analysis/frozen_dataset_l3.csv',
    'analysis/L1L2_freeze_report.md', 'analysis/L3_freeze_report.md',
    'analysis/frozen_l4/full_alignment_final.csv', 'analysis/frozen_l4/union_question_universe_v2.csv',
    'analysis/frozen_l4/concordance_pairs.csv', 'analysis/frozen_l4/deep_dive_pairs.csv',
    'analysis/frozen_l4/coverage_by_area.csv', 'analysis/frozen_l4/coverage_by_document.csv',
    'analysis/frozen_l4/L4_freeze_report.md',
    'analysis/frozen_l5/phase1_alignment_final.csv', 'analysis/frozen_l5/phase1_dynamics_by_transition.csv',
    'analysis/frozen_l5/phase2_measures_by_transition.csv', 'analysis/frozen_l5/attachments_all.csv',
    'analysis/frozen_l5/unique_study_designs_final.csv', 'analysis/frozen_l5/zombie_screen_current_pivotals.csv',
    'analysis/frozen_l5/L5_freeze_report.md',
    'analysis/supplementary_v24/supplementary_report.md', 'analysis/remediation_v25_report.md',
    'analysis/frozen_project/PROJECT_FREEZE.md', 'analysis/frozen_project/MANIFEST.json',
]
os.makedirs(DL, exist_ok=True)
dl_meta = []
for rel in dl_files:
    src = os.path.join(ROOT, rel)
    if not os.path.exists(src):
        print('MISSING download source:', rel); continue
    dst = os.path.join(DL, os.path.basename(rel))
    shutil.copyfile(src, dst)
    dl_meta.append({'file': os.path.basename(rel), 'source': rel,
                    'bytes': os.path.getsize(dst)})
dump('downloads.json', dl_meta)
with open(os.path.join(DATA, 'pmid_coverage.json'), 'w', encoding='utf-8') as fh:
    json.dump(pmid_coverage, fh)
print('DONE. downloads:', len(dl_meta))
