const request = require('supertest');
const app = require('../index');

describe('status endpoint', () => {
  test('returns ok', async () => {
    const res = await request(app).get('/status');
    expect(res.status).toBe(200);
    expect(res.body.status).toBe('ok');
    expect(res.headers['access-control-allow-origin']).toBe('*');
  });
});
