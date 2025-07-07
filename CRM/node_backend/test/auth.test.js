const fs = require('fs');
process.env.AUTH_DB = 'test_auth.db';
if (fs.existsSync(process.env.AUTH_DB)) {
  fs.unlinkSync(process.env.AUTH_DB);
}
const request = require('supertest');
const app = require('../index');
const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database(process.env.AUTH_DB);

describe('auth flow', () => {
  beforeAll(done => {
    db.serialize(() => {
      db.run(`CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        totp_secret TEXT,
        login_count INTEGER DEFAULT 0
      )`, () => {
        db.run('DELETE FROM users', done);
      });
    });
  });

  test('register and login with otp enforcement', async () => {
    const register = await request(app)
      .post('/register')
      .send({ username: 'alice', password: 'secret' });
    expect(register.status).toBe(200);
    expect(register.body.secret).toBeDefined();

    let login;
    for (let i = 0; i < 9; i++) {
      login = await request(app)
        .post('/login')
        .send({ username: 'alice', password: 'secret' });
      expect(login.status).toBe(200);
    }

    const fail = await request(app)
      .post('/login')
      .send({ username: 'alice', password: 'secret' });
    expect(fail.status).toBe(401);

    const totp = require('speakeasy').totp({
      secret: register.body.secret,
      encoding: 'base32',
    });
    const success = await request(app)
      .post('/login')
      .send({ username: 'alice', password: 'secret', otp: totp });
    expect(success.status).toBe(200);
  });

  test('login accepts form-encoded data', async () => {
    const register = await request(app)
      .post('/register')
      .send({ username: 'bob', password: 'hunter2' });
    expect(register.status).toBe(200);

    const res = await request(app)
      .post('/login')
      .type('form')
      .send({ username: 'bob', password: 'hunter2' });
    expect(res.status).toBe(200);
  });

  test('login redirects to admin for HTML requests without role', async () => {
    const register = await request(app)
      .post('/register')
      .send({ username: 'carol', password: 'pw' });
    expect(register.status).toBe(200);
    const res = await request(app)
      .post('/login')
      .set('Accept', 'text/html')
      .send({ username: 'carol', password: 'pw' });
    expect(res.status).toBe(302);
    expect(res.headers.location).toMatch(/\/core\/admin$/);
  });

  test('login redirects to specified role dashboard', async () => {
    const register = await request(app)
      .post('/register')
      .send({ username: 'dan', password: 'pw' });
    expect(register.status).toBe(200);
    const res = await request(app)
      .post('/login')
      .set('Accept', 'text/html')
      .send({ username: 'dan', password: 'pw', role: 'partner' });
    expect(res.status).toBe(302);
    expect(res.headers.location).toMatch(/\/core\/partner$/);
  });

  test('login sets auth cookie for HTML requests', async () => {
    const reg = await request(app)
      .post('/register')
      .send({ username: 'erin', password: 'pw' });
    expect(reg.status).toBe(200);
    const res = await request(app)
      .post('/login')
      .set('Accept', 'text/html')
      .send({ username: 'erin', password: 'pw' });
    expect(res.status).toBe(302);
    const cookie = res.headers['set-cookie'].join('');
    expect(cookie).toMatch(/auth=/);
  });

  afterAll(() => {
    db.close();
    if (fs.existsSync(process.env.AUTH_DB)) {
      fs.unlinkSync(process.env.AUTH_DB);
    }
  });
});
