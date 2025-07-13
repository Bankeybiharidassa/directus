import test from 'node:test';
import assert from 'node:assert/strict';
import register from '../../extensions/nucleus-suppliers/index.js';

let postRoute;
let getRoute;
const init = (_n, fn) => {
  fn({
    app: {
      post: (p, cb) => { if (p === '/suppliers') postRoute = cb; },
      get: (p, cb) => { if (p === '/suppliers') getRoute = cb; },
    },
  });
};

register({ init });

test('create and list suppliers', () => {
  const postRes = { json: (d) => { postRes.data = d; }, status: () => postRes };
  postRoute({ body: { name: 'Test' } }, postRes);
  assert.equal(postRes.data.name, 'Test');
  const listRes = { json: (d) => { listRes.data = d; } };
  getRoute({}, listRes);
  assert.ok(listRes.data.some((s) => s.id === postRes.data.id));
});
