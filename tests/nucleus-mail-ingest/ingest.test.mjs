import test from 'node:test';
import assert from 'node:assert/strict';
import register from '../../extensions/nucleus-mail-ingest/index.js';

let cronExp;
const schedule = (exp, fn) => { cronExp = exp; };
const services = { logger: { info: () => {}, error: () => {} } };

register({ schedule, services });

test('schedule cron expression', () => {
  assert.equal(cronExp, '0 * * * *');
});
