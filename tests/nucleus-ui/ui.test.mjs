import test from 'node:test';
import assert from 'node:assert/strict';
import register from '../../extensions/nucleus-ui/index.js';

let route;
const init = (_n, fn) => fn({ app: { get: (_p, cb) => { route = cb; } } });
process.env.THEME_PRIMARY = '#123456';
process.env.THEME_BG = '#654321';
register({ init });

test('theme css uses env vars', async () => {
  let mime; let text;
  const res = { type: (m) => { mime = m; return res; }, send: (t) => { text = t; } };
  route({}, res);
  assert.equal(mime, 'text/css');
  assert.ok(text.includes('--primary-color: #123456'));
  assert.ok(text.includes('--bg-color: #654321'));
});
