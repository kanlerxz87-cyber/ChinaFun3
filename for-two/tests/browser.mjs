import { chromium as playwright } from 'playwright';
import chromium from '@sparticuz/chromium';
import fs from 'node:fs/promises';
import { createRequire } from 'node:module';
import { brotliDecompressSync } from 'node:zlib';
import { execFileSync } from 'node:child_process';
import path from 'node:path';
const require=createRequire(import.meta.url);
const base=process.env.TEST_BASE_URL || 'http://127.0.0.1:3000/for-two/';
// Minimal Debian environments may lack NSS. Use the libraries shipped in the browser npm package.
const libDir=path.resolve('.cache/browser');
await fs.mkdir(libDir,{recursive:true});
await fs.writeFile(path.join(libDir,'al2023.tar'),brotliDecompressSync(await fs.readFile('node_modules/@sparticuz/chromium/bin/al2023.tar.br')));
execFileSync('tar',['-xf',path.join(libDir,'al2023.tar'),'-C',libDir]);
const browser=await playwright.launch({args:chromium.args,executablePath:await chromium.executablePath(),headless:true,env:{...process.env,LD_LIBRARY_PATH:path.join(libDir,'lib')+':'+(process.env.LD_LIBRARY_PATH||'')}});
const results=[];const errors=[];
const check=(condition,message)=>{if(!condition)throw new Error(message);results.push(message);};
await fs.mkdir('test-results',{recursive:true});
const pages=['index','hotels','dining','activities','itinerary','dates','decisions','review','sources'];
try {
 const context=await browser.newContext();
 const page=await context.newPage();
 page.on('pageerror',e=>errors.push(e.message));
 for(const width of [1440,390,320]){
  await page.setViewportSize({width,height:960});
  for(const name of pages){
   const res=await page.goto(base+name+'.html');check(res.status()===200,`${name} ${width}: loads`);
   await page.waitForLoadState('networkidle');
   const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1);
   check(!overflow,`${name} ${width}: no page overflow`);
   check(await page.locator('h1').count()===1,`${name} ${width}: one main heading`);
   if(width!==320){
    await page.addScriptTag({path:require.resolve('axe-core/axe.min.js')});
    const violations=await page.evaluate(async()=> (await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}})).violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.map(n=>({target:n.target,summary:n.failureSummary}))})));
    if(violations.length) {await fs.writeFile(`test-results/axe-${name}-${width}.json`,JSON.stringify(violations,null,2));throw new Error(`${name} ${width}: axe violations ${violations.map(v=>v.id)}`);}
    results.push(`${name} ${width}: axe WCAG A/AA checks pass`);
   }
  }
 }
 await page.setViewportSize({width:1440,height:1100});await page.goto(base);
 await page.screenshot({path:'test-results/overview-desktop.png',fullPage:true});
 await page.setViewportSize({width:390,height:844});await page.screenshot({path:'test-results/overview-mobile.png',fullPage:true,animations:'disabled'});
 await page.locator('.menu-toggle').click();check(await page.locator('.menu-toggle').getAttribute('aria-expanded')==='true','Mobile menu opens');
 await page.keyboard.press('Escape');check(await page.locator('.menu-toggle').getAttribute('aria-expanded')==='false','Escape closes mobile menu');
 await page.goto(base+'dining.html');await page.locator('[data-filter="starred"]').click();check(await page.locator('tbody tr:visible').count()===5,'Star filter has five restaurants');
 await page.locator('input[type=search]').fill('Polux');check(await page.locator('tbody tr:visible').count()===0,'Search combines with category');check(await page.locator('.empty-results').isVisible(),'Empty-state feedback shown');
 await page.locator('[data-filter="all"]').click();check(await page.locator('tbody tr:visible').count()===1,'All filter restores matching Polux');
 await page.goto(base+'dining.html?cluster=Xintiandi');check(await page.locator('tbody tr:visible').count()===2,'Dashboard cluster deep link filters correctly');
 await page.goto(base+'hotels.html');await page.locator('[data-save="peninsula"]').click();await page.reload();check(await page.locator('[data-save="peninsula"]').getAttribute('aria-pressed')==='true','Hotel shortlist persists locally');
 await page.goto(base+'decisions.html');await page.locator('[data-suggestion="S01"] [data-choice="consider"]').click();await page.reload();check(await page.locator('[data-suggestion="S01"] [data-choice="consider"]').getAttribute('aria-pressed')==='true','Suggestion preference persists locally');
 const downloadPromise=page.waitForEvent('download');await page.locator('#export-decisions').click();const download=await downloadPromise;await download.saveAs('test-results/review-export.json');
 const exported=JSON.parse(await fs.readFile('test-results/review-export.json','utf8'));check(exported.suggestions.S01==='consider','Review export contains selected proposal');check(exported.savedHotelIds.includes('peninsula'),'Review export includes saved candidate');
 const nojs=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:844}});const plain=await nojs.newPage();await plain.goto(base+'dining.html');check(await plain.locator('tbody tr').count()===7,'All dining records render without JavaScript');check(await plain.locator('a[href^="https://guide.michelin.com"]').count()>0,'Official links available without JavaScript');await nojs.close();
 check(errors.length===0,'No browser JavaScript errors');
 await fs.writeFile('test-results/browser-report.json',JSON.stringify({status:'passed',checks:results.length,results},null,2));console.log(`PASS: ${results.length} browser checks`);
} finally {await browser.close();}
