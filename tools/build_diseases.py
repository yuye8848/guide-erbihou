#!/usr/bin/env python3
"""Build data/diseases.json — the "Disease panorama" page data — from the
site's generated data files: data/questions.json (L4 union universe),
data/items.json (current-version recommendations with L3 fields) and
data/changes.json (L5 flips / dropped, built by tools/build_changes.py).

A question's 'areas' field is a semicolon list that may repeat a slug within
one question; slugs are deduplicated per question before counting. Member
recommendations are deduplicated per area. Members carry L4-substrate rec
ids (e.g. AAO2014TIN-02A) while items.json carries L3 rec ids
(AAO2014TIN-KAS02A); the join uses the frozen parse_key normalisation (the
same rule as tools/build_data.py). Members whose rec resolves to no
items.json entry — prior-version recs and NICE recs (bare section numbers) —
are counted in n_member_recs / unjoined_n and excluded from the item-joined
statistics (direction counts, pivotal designs, fragile count, the item
table) — nothing silently vanishes.

Per-area question counts are ASSERTED against the frozen L4 coverage counts.

Run AFTER tools/build_data.py and tools/build_changes.py:
  python3 site/tools/build_diseases.py
Output: site/data/diseases.json
"""
import json, os
from collections import Counter

SITE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA = os.path.join(SITE, 'data')

def load(name):
    with open(os.path.join(DATA, name), encoding='utf-8') as fh:
        return json.load(fh)

NAMES = {
    'rhinosinusitis': ('Rhinosinusitis', '鼻窦炎'),
    'skull_base_and_tumours': ('Skull base & tumours', '颅底与肿瘤'),
    'sleep_apnoea': ('Sleep apnoea', '睡眠呼吸暂停'),
    'allergic_rhinitis': ('Allergic rhinitis', '变应性鼻炎'),
    'otitis_media': ('Otitis media', '中耳炎'),
    'hearing': ('Hearing', '听力'),
    'olfaction': ('Olfaction', '嗅觉'),
    'tinnitus': ('Tinnitus', '耳鸣'),
    'vertigo_balance': ('Vertigo & balance', '眩晕与平衡'),
    'voice': ('Voice', '嗓音'),
    'sore_throat': ('Sore throat', '咽喉痛'),
    'tonsil': ('Tonsils', '扁桃体'),
    'epistaxis': ('Epistaxis', '鼻出血'),
    'facial_nerve': ('Facial nerve', '面神经'),
    'earwax': ('Earwax', '耵聍'),
    'neck_mass': ('Neck mass', '颈部包块'),
    'opioid': ('Opioids', '阿片类'),
    'ait': ('Allergen immunotherapy', '变应原免疫治疗'),
    'rhinoplasty': ('Rhinoplasty', '鼻整形'),
    'otitis_externa': ('Otitis externa', '外耳炎'),
}
EXPECTED_Q = {
    'rhinosinusitis': 138, 'skull_base_and_tumours': 123, 'sleep_apnoea': 119,
    'allergic_rhinitis': 116, 'otitis_media': 77, 'hearing': 56,
    'olfaction': 52, 'tinnitus': 50, 'vertigo_balance': 31, 'voice': 28,
    'sore_throat': 18, 'tonsil': 16, 'epistaxis': 16, 'facial_nerve': 13,
    'earwax': 12, 'neck_mass': 12, 'opioid': 12, 'ait': 11,
    'rhinoplasty': 10, 'otitis_externa': 8,
}

def parse_key(rec_id):
    """Frozen L1/L2 <-> L3 join key (same rule as tools/build_data.py)."""
    if '-' not in rec_id:
        return None
    doc, suf = rec_id.rsplit('-', 1)
    if suf.startswith('KAS'):
        suf = suf[3:]
    num = ''
    while suf and suf[0].isdigit():
        num += suf[0]; suf = suf[1:]
    return (doc, (int(num) if num else 0, suf.upper()))

questions = load('questions.json')
items = load('items.json')
changes = load('changes.json')
item_by_key = {}
for i in items:
    k = parse_key(i['rec'])
    assert k not in item_by_key, ('parse_key collision in items.json', k)
    item_by_key[k] = i

area_questions = {}
for q in questions:
    slugs = []
    for a in (q.get('areas') or '').split(';'):
        a = a.strip()
        if a and a not in slugs:
            slugs.append(a)
    for a in slugs:
        area_questions.setdefault(a, []).append(q)

assert set(area_questions) == set(EXPECTED_Q), (
    'area set mismatch', sorted(set(area_questions) ^ set(EXPECTED_Q)))
for slug, exp in EXPECTED_Q.items():
    assert len(area_questions[slug]) == exp, (slug, len(area_questions[slug]), exp)
print('area question counts asserted for all 20 areas')

all_flips = changes['flips'] + changes['aria']['flips']
all_dropped = changes['dropped'] + changes['aria']['dropped']

areas = []
total_unjoined = 0
for slug in sorted(EXPECTED_Q, key=lambda s: -EXPECTED_Q[s]):
    qs = area_questions[slug]
    pairs = [(m['doc'], m['rec']) for q in qs for m in q['members']]
    recs = sorted({rec for _, rec in pairs})
    docs = sorted({doc for doc, _ in pairs})
    docset = set(docs)
    resolved = {}
    for r in recs:
        it = item_by_key.get(parse_key(r))
        if it:
            resolved[r] = it
    joined_by_rec = {it['rec']: it for it in resolved.values()}
    joined = list(joined_by_rec.values())
    unjoined_n = len(recs) - len(resolved)
    total_unjoined += unjoined_n
    areas.append({
        'slug': slug, 'name_en': NAMES[slug][0], 'name_zh': NAMES[slug][1],
        'n_questions': len(qs),
        'recs': recs, 'n_member_recs': len(recs),
        'n_items': len(joined), 'unjoined_n': unjoined_n,
        'docs': docs, 'n_docs': len(docs),
        'direction_counts': dict(Counter(i['direction'] or 'none' for i in joined)),
        'pivotal_design_counts': dict(Counter(i['pivotal_design'] or 'none' for i in joined)),
        'fragile_n': sum(1 for i in joined if i['fragile']),
        'single_coverage_questions': sum(1 for q in qs if q['n_docs'] == 1),
        'flips_n': sum(1 for f in all_flips
                       if f['prior_doc'] in docset or f['current_doc'] in docset),
        'dropped_n': sum(1 for d in all_dropped if d['prior_doc'] in docset),
        'qids': [q['qid'] for q in qs],
        'items': [{'rec': i['rec'], 'doc': i['doc'], 'guideline': i['guideline'],
                   'year': i['year'], 'direction': i['direction'],
                   'tier': i['tier'], 'fragile': i['fragile']}
                  for i in sorted(joined, key=lambda x: (x['doc'], x['rec']))],
    })

out = {'areas': areas,
       'totals': {'areas': len(areas), 'questions': len(questions),
                  'unjoined_member_recs_across_areas': total_unjoined},
       'source': 'Generated by site/tools/build_diseases.py from data/questions.json + '
                 'data/items.json + data/changes.json (themselves generated from the '
                 'frozen datasets by tools/build_data.py and tools/build_changes.py).'}
with open(os.path.join(DATA, 'diseases.json'), 'w', encoding='utf-8') as fh:
    json.dump(out, fh, ensure_ascii=False, separators=(',', ':'))
print('wrote data/diseases.json | areas', len(areas),
      '| unjoined member recs across areas (with cross-area multiplicity):', total_unjoined)
for a in areas:
    print(' ', a['slug'], 'q', a['n_questions'], 'member_recs', a['n_member_recs'],
          'joined', a['n_items'], 'unjoined', a['unjoined_n'], 'docs', a['n_docs'],
          'fragile', a['fragile_n'], 'flips', a['flips_n'], 'dropped', a['dropped_n'])
