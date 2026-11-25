import json
import subprocess
import unittest
from datetime import date, timedelta
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'considered'
D = json.loads((ROOT / 'research/data.json').read_text())
PAGES = ['index','hotels','restaurants','activities','itinerary','dates','review','suggestions','sources']

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links=[]; self.ids=[]; self.lang=None; self.viewport=False
        self.headings=0; self.current=[]; self.in_row=False; self.row_links=[]; self.rows=[]
        self.in_body=False; self.in_tbody=False
        self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag=='html': self.lang=a.get('lang')
        if tag=='meta' and a.get('name')=='viewport': self.viewport=True
        if tag=='h1': self.headings+=1
        if tag=='a':
            self.links.append(a.get('href',''))
            if a.get('aria-current')=='page': self.current.append(a.get('href'))
            if self.in_row: self.row_links.append(a.get('href',''))
        if tag in ('script','link'):
            self.links.append(a.get('src',a.get('href','')))
        if tag=='tbody': self.in_tbody=True
        if tag=='tr' and self.in_tbody: self.in_row=True; self.row_links=[]
    def handle_endtag(self,tag):
        if tag=='tr' and self.in_row:
            self.rows.append(self.row_links); self.in_row=False
        if tag=='tbody': self.in_tbody=False

class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run(['python3','scripts/build.py'],cwd=ROOT,check=True)
        cls.pages={p:Page((SITE/(p+'.html')).read_text()) for p in PAGES}
    def test_nine_pages_accessible_shell(self):
        for key,p in self.pages.items():
            with self.subTest(page=key):
                self.assertEqual(p.lang,'en')
                self.assertTrue(p.viewport)
                self.assertEqual(p.headings,1)
                self.assertEqual(p.current,[key+'.html'])
                self.assertIn('main',p.ids)
                self.assertEqual(len(p.ids),len(set(p.ids)))
    def test_internal_links_and_fragments(self):
        for key,p in self.pages.items():
            for href in p.links:
                with self.subTest(page=key,href=href):
                    u=urlsplit(href)
                    if u.scheme or u.netloc: continue
                    self.assertFalse(href.startswith('/'),'Root-absolute URLs break project Pages')
                    target=SITE / unquote(u.path or key+'.html')
                    self.assertTrue(target.is_file(),href)
                    if u.fragment and target.suffix=='.html':
                        self.assertIn(u.fragment,Page(target.read_text()).ids)
    def test_each_table_row_has_primary_source(self):
        official={urlsplit(s['url']).hostname for s in D['sources'].values() if s['kind']=='official'}
        for key,p in self.pages.items():
            for i,links in enumerate(p.rows):
                self.assertTrue(any(urlsplit(h).hostname in official for h in links),(key,i))
    def test_unknown_values_not_fabricated(self):
        for h in D['hotels']:
            self.assertIsNone(h['total']); self.assertIsNone(h['rank']); self.assertIsNone(h['transitCount'])
        self.assertIsNone(next(h for h in D['hotels'] if h['id']=='radisson')['bath'])
        for a in D['activities']: self.assertIsNone(a['total'])
        for r in D['restaurants']:
            if r['id']!='tang': self.assertIsNone(r['total'])
    def test_distinctions_and_explicit_totals(self):
        self.assertEqual(len(D['restaurants']),6)
        self.assertEqual(sum(r['stars']>0 for r in D['restaurants']),5)
        tavern=next(r for r in D['restaurants'] if r['id']=='tavern')
        self.assertEqual(tavern['stars'],0)
        self.assertIn('no star',tavern['distinction'])
        tang=next(r for r in D['restaurants'] if r['id']=='tang')
        self.assertEqual(tang['total'],'CNY 888 lunch / CNY 2,288 all-day')
    def test_source_records_and_scope(self):
        for collection in ['hotels','restaurants','activities']:
            for item in D[collection]:
                self.assertTrue(item['sources'])
                self.assertTrue(any(D['sources'][s]['kind']=='official' for s in item['sources']))
                for s in item['sources']: self.assertIn(s,D['sources'])
        for s in D['sources'].values():
            self.assertEqual(s['checked'],'2026-11-25')
            self.assertTrue(s['url'].startswith('https://'))
            self.assertTrue(s['observed'])
    def test_calendar_arithmetic(self):
        first=date(2027,2,15); last=date(2027,3,23)
        self.assertEqual((date(2027,2,18)-first).days,3)
        self.assertEqual((last-timedelta(days=7)-first).days+1,30)
        text=(SITE/'dates.html').read_text()
        for i in range(30):
            start=first+timedelta(days=i)
            self.assertIn(f'{start.isoformat()} → {(start+timedelta(days=7)).isoformat()}',text)
    def test_deterministic_build(self):
        before={p:(SITE/(p+'.html')).read_bytes() for p in PAGES}
        subprocess.run(['python3','scripts/build.py'],cwd=ROOT,check=True)
        for p in PAGES: self.assertEqual(before[p],(SITE/(p+'.html')).read_bytes())

if __name__=='__main__': unittest.main()
