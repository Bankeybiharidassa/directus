import test from 'node:test';
import assert from 'node:assert/strict';
import register from '../../extensions/nucleus-docs/index.js';

let route;
const app = { post: (_path, cb) => { route = cb; } };
const init = (_name, fn) => { fn({ app }); };

register({ init });

test('generate csv', async () => {
  let mime;
  let sent;
  const res = {
    type: (m) => { mime = m; return res; },
    send: (d) => { sent = d; }
  };
  await route({ body: { type: 'csv', data: [{ id: 1 }] } }, res);
  assert.equal(mime, 'text/csv');
  assert.match(String(sent), /id/);
});

test('generate pdf', async () => {
  let mime;
  let len = 0;
  const res = {
    type: (m) => { mime = m; return res; },
    send: (d) => { len = d.length; }
  };
  await route({ body: { type: 'pdf', data: { hello: 'world' } } }, res);
  assert.equal(mime, 'application/pdf');
  assert.ok(len > 0);
});
