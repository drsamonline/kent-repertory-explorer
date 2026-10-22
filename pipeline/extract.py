#!/usr/bin/env python3
"""Extract Kent 1897 (graded) from the OOReP PostgreSQL dump into a compact tree JSON.

Source : oorep.sql (COPY blocks)  -- repertory abbrev "publicum" = English Kent
Output : kent/kent.json  { book, remedies[], tree{name, children[], links[]} }
Grades : rubricremedy.weight  (1 / 2 / 3)  -- Kent's three typeface grades
"""
import json, os, sys, collections

SRC = '/tmp/oorep.sql'
OUT = '/scratch/work/kent/kent.json'
REP = 'publicum'
TERM = '\\' + '.'

def block(path, table):
    out, f = [], False
    with open(path, encoding='utf-8', errors='replace') as fh:
        for line in fh:
            if not f:
                if line.startswith('COPY public.%s ' % table):
                    f = True
                continue
            s = line.rstrip('\n')
            if s == TERM:
                break
            out.append(s)
    return out

def main():
    print('reading remedy ...'); rem_rows = block(SRC, 'remedy')
    print('reading rubric ...'); rub_rows = block(SRC, 'rubric')
    print('reading rubricremedy ...'); rr_rows = block(SRC, 'rubricremedy')

    # remedy id -> (abbrev, long name)
    rem = {}
    for x in rem_rows:
        p = x.split('\t')
        if len(p) < 3: continue
        try: rid = int(p[0])
        except ValueError: continue
        ab = p[1].strip(); ln = p[2].strip()
        rem[rid] = (ab, ln if ln and ln != r'\N' else ab)

    # rubric id -> fullpath  (only our repertory)
    paths = {}
    for x in rub_rows:
        if not x.startswith(REP + '\t'): continue
        p = x.split('\t')
        if len(p) < 6: continue
        try: rid = int(p[1])
        except ValueError: continue
        fp = p[5].strip()
        if fp and fp != r'\N':
            paths[rid] = fp
    print('rubrics with a path:', len(paths))

    # rubric id -> [(remedyid, grade)]
    links = collections.defaultdict(list)
    for x in rr_rows:
        if not x.startswith(REP + '\t'): continue
        p = x.split('\t')
        if len(p) < 4: continue
        try: rid = int(p[1]); mid = int(p[2]); w = int(p[3])
        except ValueError: continue
        if w < 1 or w > 3: w = 1
        if rid in paths and mid in rem:
            links[rid].append((mid, w))
    print('rubric link sets:', len(links), 'total links:', sum(len(v) for v in links.values()))

    # compact remedy table: only remedies that are actually used
    used = sorted({m for v in links.values() for m, _ in v})
    ridx = {m: i for i, m in enumerate(used)}
    remedy_table = [list(rem[m]) for m in used]
    print('remedies used:', len(remedy_table))

    # build the prefix-shared tree from fullpaths
    root = {'n': '', 'c': {}, 'l': None}
    def child(node, name):
        if name not in node['c']:
            node['c'][name] = {'n': name, 'c': {}, 'l': None}
        return node['c'][name]

    for rid, fp in paths.items():
        segs = [s.strip() for s in fp.split(',') if s.strip()]
        if not segs: continue
        node = root
        for s in segs:
            node = child(node, s)
        node['l'] = sorted(links.get(rid, []), key=lambda t: (-t[1], t[0]))

    # serialise: children as arrays, links as [remedyIdx, grade] pairs
    DIG = '0123456789abcdefghijklmnopqrstuvwxyz'
    def b36(x):
        s = ''
        while x:
            s = DIG[x % 36] + s; x //= 36
        return s or '0'

    emitted_rubrics = [0]
    def ser(node):
        o = {'n': node['n']}
        if node['c']:
            o['c'] = [ser(node['c'][k]) for k in sorted(node['c'])]
        if node['l']:
            emitted_rubrics[0] += 1
            # pack (remedyIdx*4 + grade) as 3-char base36 -> ~2x smaller than JSON pairs
            o['r'] = ''.join(b36(ridx[m] * 4 + w).rjust(3, '0') for m, w in node['l'])
            o['k'] = len(node['l'])
        return o

    tree = ser(root)
    out = {
        'book': {
            'id': 'repertorium-publicum-2008',
            'title': 'Repertorium Publicum',
            'author': 'Vladimir Polony',
            'year': 2008,
            'edition': '0.5',
            'license': 'GPL v3 - as part of the OpenRep source code',
            'note': 'An open, Kent-derived repertory. Not Kent 1897 first edition.',
            'source': 'OOReP open repertory database — repertory token "publicum"',
        },
        'remedies': remedy_table,
        'tree': tree,
        'counts': {
            'rubrics': emitted_rubrics[0],
            'rubric_paths': sum(1 for _ in paths),
            'remedy_links': sum(len(v) for v in links.values()),
            'remedies': len(remedy_table),
        },
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, ensure_ascii=False, separators=(',', ':'))
    print('wrote', OUT, os.path.getsize(OUT), 'bytes')

if __name__ == '__main__':
    main()
