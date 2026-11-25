// Optional browser tests. Install playwright and @sparticuz/chromium without committing node_modules.
const { chromium: playwright } = require('playwright');
const chromium = require('@sparticuz/chromium').default;
const assert = require('node:assert/strict');
(async () => {
  const path = require('node:path');
  const { inflate } = require('@sparticuz/chromium');
  const libs = await inflate(path.join(path.dirname(require.resolve('@sparticuz/chromium')), '../bin/al2023.tar.br'));
  const browser = await playwright.launch({executablePath: await chromium.executablePath(), args: chromium.args, headless:true, env: {...process.env, LD_LIBRARY_PATH: `${libs}/lib:${process.env.LD_LIBRARY_PATH || ''}`}});
  const pages = ['index','hotels','restaurants','activities','itinerary','dates','review','suggestions','sources'];
  const errors=[];
  const page=await browser.newPage();
  page.on('pageerror', error => errors.push(String(error)));
  for (const width of [390, 768, 1440]) {
    await page.setViewportSize({width, height:1000});
    for(const key of pages) {
      const response=await page.goto(`http://127.0.0.1:8000/considered/${key}.html`);
      assert.equal(response.status(),200);
      assert.equal(await page.locator('h1').count(),1);
      assert.equal(await page.locator('nav a[aria-current="page"]').count(),1);
      const overflow=await page.evaluate(()=>document.documentElement.scrollWidth > window.innerWidth + 1);
      assert.equal(overflow,false,`${key} overflows viewport at ${width}`);
    }
  }
  await page.goto('http://127.0.0.1:8000/considered/restaurants.html');
  await page.getByRole('button',{name:'Selected, no star', exact:true}).click();
  assert.equal(await page.locator('tbody tr:visible').count(),1);
  assert.match(await page.locator('tbody tr:visible').innerText(),/Shanghai Tavern/);
  await page.getByRole('button',{name:'Starred',exact:true}).click();
  assert.equal(await page.locator('tbody tr:visible').count(),5);
  await page.getByRole('button',{name:'All entries',exact:true}).click();
  await page.locator('.table-search').fill('unmatchable-test-value');
  assert.equal(await page.locator('tbody tr:visible').count(),0);
  assert.equal(await page.locator('.no-results').isVisible(),true);
  await page.locator('.table-search').fill('Changning');
  assert.equal(await page.locator('tbody tr:visible').count(),2);
  await page.goto('http://127.0.0.1:8000/considered/suggestions.html');
  await page.locator('#clear-choices').click();
  await page.locator('[data-choice="quotes"]').click();
  assert.equal(await page.locator('[data-choice="quotes"]').getAttribute('aria-pressed'),'true');
  await page.reload();
  assert.equal(await page.locator('[data-choice="quotes"]').getAttribute('aria-pressed'),'true');
  await page.locator('#clear-choices').click();
  assert.equal(await page.locator('[data-choice="quotes"]').getAttribute('aria-pressed'),'false');
  await page.getByText('What is the actual time away?',{exact:true}).click();
  assert.equal(await page.locator('details').first().getAttribute('open'),'');
  await page.setViewportSize({width:1440,height:1100});
  await page.goto('http://127.0.0.1:8000/considered/index.html');
  await page.screenshot({path:'.cache/dashboard-desktop.png',fullPage:true});
  await page.setViewportSize({width:390,height:844});
  await page.screenshot({path:'.cache/dashboard-mobile.png',fullPage:true});
  await page.goto('http://127.0.0.1:8000/considered/restaurants.html');
  await page.screenshot({path:'.cache/dining-mobile.png',fullPage:true});
  assert.deepEqual(errors,[],'No browser runtime errors');
  console.log('PASS: 27 page/viewport checks, table filters/search, no-results, saved/cleared review choices, disclosure, no runtime errors.');
  await browser.close();
})().catch(error=>{console.error(error);process.exit(1)});
