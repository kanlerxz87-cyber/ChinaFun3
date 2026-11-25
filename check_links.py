#!/usr/bin/env python3
"""Verify every internal link/href in the generated pages resolves to a file."""
import re, sys, pathlib
root = pathlib.Path(__file__).parent / 'plan'
pages = sorted(root.glob('*.html'))
bad = []
for p in pages:
    s = p.read_text(encoding='utf-8')
    for href in re.findall(r'href="([^"]+)"', s):
        if href.startswith(('http://', 'https://', 'mailto:', 'tel:', '#')):
            continue
        target = (root / href.split('#')[0]).resolve()
        if not target.exists():
            bad.append(f'{p.name} -> {href}')
    if '<table' in s:
        for tbl in re.findall(r'<table>.*?</table>', s, re.S):
            heads = len(re.findall(r'<th[ >]', tbl))
            for row in re.findall(r'<tr>(.*?)</tr>', tbl, re.S):
                cells = len(re.findall(r'<td[ >]', row))
                if cells and heads and cells != heads:
                    bad.append(f'{p.name}: table row has {cells} cells vs {heads} headers')
print(f'checked {len(pages)} pages')
print('\n'.join(sorted(set(bad))) or 'no problems found')
sys.exit(1 if bad else 0)
