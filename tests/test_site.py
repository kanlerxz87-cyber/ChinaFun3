import unittest,json,re
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from datetime import date
from decimal import Decimal
ROOT=Path(__file__).resolve().parents[1]
D=json.loads((ROOT/'data/trip.json').read_text())
S={s['id']:s for s in D['sources']}
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__();self.ids=[];self.links=[];self.h1=0;self.lang=None;self.images=[];self.targets=[];self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='html':self.lang=a.get('lang')
        if tag=='h1':self.h1+=1
        if tag in ('a','link') and 'href' in a:self.links.append(a['href'])
        if tag in ('script','img') and 'src' in a:self.links.append(a['src'])
        if tag=='img':self.images.append(a)
        if a.get('target')=='_blank':self.targets.append(a)
class Tests(unittest.TestCase):
    def test_unique_sources(self):
        self.assertEqual(len(S),len(D['sources']))
        for s in S.values():
            self.assertTrue(s['url'].startswith('https://'));self.assertTrue(s['evidence']);self.assertEqual(s['checked'],'2026-11-25')
    def test_all_venue_rows_have_official_evidence(self):
        for section in ['hotels','restaurants','activities','quotes']:
            ids=[]
            for row in D[section]:
                ids.append(row['id']);self.assertTrue(row['sources'])
                self.assertTrue(any(S[x]['kind']=='official' for x in row['sources']))
                for x in row['sources']:self.assertIn(x,S)
                for x in row.get('media',[]):self.assertEqual(S[x]['kind'],'media')
            self.assertEqual(len(ids),len(set(ids)))
    def test_unknowns_not_invented(self):
        for h in D['hotels']:
            self.assertIsNone(h['rank']);self.assertIsNone(h['within60']);self.assertIsNone(h['privateBathroom'])
        for r in D['restaurants']+D['activities']:
            self.assertIsNone(r['minutes']);self.assertIsNone(r['price2027'])
        self.assertEqual(sum(h['total'] is not None for h in D['hotels']),1)
    def test_quote_dates_occupancy_and_math(self):
        self.assertEqual(len(D['quotes']),6)
        for q in D['quotes']:
            self.assertEqual((date.fromisoformat(q['checkOut'])-date.fromisoformat(q['checkIn'])).days,7)
            self.assertGreaterEqual(q['checkIn'],'2027-02-15');self.assertLessEqual(q['checkOut'],'2027-03-23')
            self.assertEqual(q['adults'],2);self.assertEqual(q['rooms'],1)
            self.assertEqual(q['subtotal'],q['nightly']*7)
            self.assertEqual(Decimal(str(q['total'])),Decimal(q['subtotal'])*Decimal('1.166'))
            self.assertIsNone(q['checkoutTotal'])
        self.assertEqual(sum(q['total']==20119.33 for q in D['quotes']),3)
    def test_dining_distinctions_and_totals(self):
        r={x['id']:x for x in D['restaurants']}
        self.assertEqual(sum(x['stars']>0 for x in r.values()),5)
        self.assertEqual(r['polux']['distinction'],'Bib Gourmand');self.assertEqual(r['polux']['stars'],0)
        self.assertEqual(r['sir']['distinction'],'Selected');self.assertEqual(r['sir']['stars'],0)
        self.assertEqual(r['bao']['priceNow'],[1788*2,(1788+800)*2])
        self.assertEqual(r['yi']['priceNow'],[round(338*2*1.166,2)])
        self.assertEqual(r['sir']['priceNow'],[round(1288*2*1.166,2)])
        self.assertIsNone(r['tang']['days'])
    def test_internal_links_and_fragments(self):
        pages={f.name:Page(f.read_text()) for f in ROOT.glob('*.html')}
        self.assertEqual(len(pages),10)
        for name,p in pages.items():
            for href in p.links:
                parsed=urlsplit(href)
                if parsed.scheme or parsed.netloc:continue
                path=unquote(parsed.path) or name
                self.assertFalse(path.startswith('/'),f'Base-path unsafe: {href}')
                target=ROOT/path
                self.assertTrue(target.exists(),f'{name}: missing {href}')
                if parsed.fragment and path.endswith('.html'):
                    self.assertIn(unquote(parsed.fragment),pages[path].ids,f'{name}: missing fragment {href}')
    def test_html_basics(self):
        for f in ROOT.glob('*.html'):
            p=Page(f.read_text());self.assertEqual(p.lang,'en');self.assertEqual(p.h1,1)
            self.assertEqual(len(p.ids),len(set(p.ids)),f.name)
            for a in p.images:self.assertIn('alt',a)
            for a in p.targets:self.assertIn('noopener',a.get('rel',''))
    def test_source_policy_visible(self):
        for f in ['hotels.html','dining.html','activities.html','dates.html']:
            text=(ROOT/f).read_text();self.assertIn('Not verified' if f!='dates.html' else 'checkout',text)
        self.assertIn('No fabricated ranking',(ROOT/'hotels.html').read_text())
        self.assertIn('Lowest observed ≠ guaranteed cheapest',(ROOT/'dates.html').read_text())
    def test_no_runtime_remote_dependencies(self):
        css=(ROOT/'assets/style.css').read_text();self.assertNotIn('@import',css)
        for f in ROOT.glob('*.html'):
            self.assertNotRegex(f.read_text(),r'<script[^>]+src="https?://')
if __name__=='__main__':unittest.main()
