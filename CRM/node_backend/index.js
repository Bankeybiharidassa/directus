const express = require('express');
const bcrypt = require('bcryptjs');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const speakeasy = require('speakeasy');
const cors = require('cors');

function log(level, msg) {
  const ts = new Date().toISOString();
  console.log(`${ts} ${level} ${msg}`);
}

const dbPath = process.env.AUTH_DB || path.join(__dirname, 'auth.db');
const db = new sqlite3.Database(dbPath);

db.serialize(() => {
  db.run(`CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    totp_secret TEXT,
    login_count INTEGER DEFAULT 0
  )`);
});

const app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cors());
app.use((req, res, next) => {
  log('INFO', `${req.method} ${req.url}`);
  next();
});

app.post('/register', (req, res) => {
  const { username, password } = req.body;
  if (!username || !password) {
    return res.status(400).json({ error: 'Username and password required' });
  }
  log('INFO', `register ${username}`);
  const hash = bcrypt.hashSync(password, 10);
  const secret = speakeasy.generateSecret({ length: 20 }).base32;
  db.run(
    'INSERT INTO users (username, password, totp_secret) VALUES (?, ?, ?)',
    [username, hash, secret],
    function (err) {
      if (err) {
        return res.status(400).json({ error: 'User exists' });
      }
      res.json({ id: this.lastID, secret });
    }
  );
});

app.post('/login', (req, res) => {
  const { username, password, otp } = req.body;
  if (!username || !password) {
    return res.status(400).json({ error: 'Missing credentials' });
  }
  log('INFO', `login ${username}`);
  db.get('SELECT * FROM users WHERE username = ?', [username], (err, user) => {
    if (err || !user) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    if (!bcrypt.compareSync(password, user.password)) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    const needsOtp = user.login_count >= 9;
    if (needsOtp) {
      if (!otp) {
        return res.status(401).json({ error: 'OTP required' });
      }
      const valid = speakeasy.totp.verify({
        secret: user.totp_secret,
        encoding: 'base32',
        token: otp,
      });
      if (!valid) {
        return res.status(401).json({ error: 'Invalid OTP' });
      }
      db.run('UPDATE users SET login_count = 0 WHERE id = ?', [user.id]);
    } else {
      db.run('UPDATE users SET login_count = login_count + 1 WHERE id = ?', [user.id]);
    }
    const accept = req.headers['accept'] || '';
    if (accept.includes('text/html')) {
      const host = (req.headers['host'] || '').split(':')[0] || 'localhost';
      const role = req.body.role || 'admin';
      const allowed = ['admin', 'support', 'distributor', 'partner', 'enduser', 'company'];
      const target = allowed.includes(role) ? role : 'admin';
      const token = Buffer.from(`${username}:${password}`).toString('base64');
      res.cookie('auth', token, { httpOnly: true });
      return res.redirect(`http://${host}:8000/core/${target}`);
    }
    res.json({ message: 'Logged in' });
  });
});

app.get('/status', (req, res) => {
  res.json({ status: 'ok' });
});

if (require.main === module) {
  const port = process.env.PORT || 3001;
  app.listen(port, () => log('INFO', `Node auth server listening on ${port}`));
}

module.exports = app;
