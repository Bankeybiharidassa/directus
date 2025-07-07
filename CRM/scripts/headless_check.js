const fs = require('fs');
const puppeteer = require('../node_backend/node_modules/puppeteer');
const fetch = (...args) => import('../node_backend/node_modules/node-fetch/src/index.js').then(m => m.default(...args));

async function ensureUser(username, password) {
  try {
    await fetch('http://127.0.0.1:3001/register', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ username, password })
    });
  } catch (err) {
    // ignore errors (user may exist)
  }
}

async function loginAndCapture(role, username, password) {
  const browser = await puppeteer.launch({ args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.goto(`http://127.0.0.1:8000/core/login?role=${role}`);
  await page.type('input[name="username"]', username);
  await page.type('input[name="password"]', password);
  await page.click('button[type="submit"]');
  await page.waitForNavigation();
  await page.screenshot({ path: `logs/${role}_dashboard.png` });
  const links = await page.evaluate(() => Array.from(document.querySelectorAll('a')).map(a => ({text: a.innerText, href: a.getAttribute('href')})));
  fs.writeFileSync(`logs/browser_${role}.json`, JSON.stringify(links, null, 2));
  await browser.close();
}

(async () => {
  const roles = [
    ['admin', 'test-admin', 'admin123'],
    ['support', 'test-supporter', 'support123'],
    ['company', 'test-employee', 'employee123'],
    ['distributor', 'test-distributor', 'distrib123'],
    ['partner', 'test-partner', 'partner123'],
    ['enduser', 'test-enduser', 'enduser123'],
  ];
  for (const [role, user, pass] of roles) {
    await ensureUser(user, pass);
    await loginAndCapture(role, user, pass);
  }
})();
