import test from 'node:test';
import assert from 'node:assert/strict';
import register from '../../extensions/nucleus-contracts/index.js';

let createRoute; let termRoute;
const init = (_n, fn) => {
  fn({
    app: {
      post: (p, cb) => {
        if (p === '/contracts') createRoute = cb;
        if (p === '/contracts/:id/terminate') termRoute = cb;
      },
      get: () => {},
    },
  });
};

register({ init });

test('terminate contract', () => {
  const createRes = { json: (d) => { createRes.data = d; }, status: () => createRes };
  createRoute({ body: { name: 'Deal' } }, createRes);
  const id = createRes.data.id;
  const termRes = { json: (d) => { termRes.data = d; }, status: (c) => { termRes.code = c; return termRes; } };
  termRoute({ params: { id: String(id) } }, termRes);
  assert.equal(termRes.data.status, 'terminated');
});
