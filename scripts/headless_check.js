#!/usr/bin/env node
// Proxy to CRM headless check script
const { spawnSync } = require('child_process');
const path = require('path');
const target = path.join(__dirname, '../CRM/scripts/headless_check.js');
spawnSync('node', [target], { stdio: 'inherit' });
