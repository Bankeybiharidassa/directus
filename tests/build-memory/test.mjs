import test from 'node:test';
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const env = {
  ...process.env,
  DB_CLIENT: 'sqlite3',
  DB_FILENAME: ':memory:',
  HOST: '127.0.0.1',
  PORT: '8055',
};

const rootDir = dirname(dirname(dirname(fileURLToPath(import.meta.url))));
const nodeBin = process.execPath;
let sqliteAvailable = true;
try {
  require('sqlite3');
} catch {
  sqliteAvailable = false;
}

function run(cmd, args, options = {}) {
  return new Promise((resolve, reject) => {
    const proc = spawn(cmd, args, { stdio: 'inherit', cwd: rootDir, ...options });
    proc.on('exit', code => (code === 0 ? resolve() : reject(new Error(`${cmd} failed with code ${code}`))));
  });
}

function runCli(args, options = {}) {
  return run(nodeBin, [join(rootDir, 'directus/cli.js'), ...args], options);
}

function waitForOutput(proc, regex, timeout = 10000) {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => {
      proc.kill();
      reject(new Error('timeout waiting for server start'));
    }, timeout);
    proc.stdout.on('data', data => {
      if (regex.test(data.toString())) {
        clearTimeout(timer);
        resolve();
      }
    });
    proc.stderr.on('data', data => {
      if (regex.test(data.toString())) {
        clearTimeout(timer);
        resolve();
      }
    });
  });
}

test('build and start with in-memory sqlite', { skip: !sqliteAvailable }, async () => {
  await run('pnpm', ['build'], { env });
  await runCli(['bootstrap'], { env });
  const server = spawn(nodeBin, [join(rootDir, 'directus/cli.js'), 'start'], { env });
  await waitForOutput(server, /Server started/);
  server.kill();
  assert.ok(true);
});
