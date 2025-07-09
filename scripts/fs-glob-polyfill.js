import fs from 'node:fs/promises';
import path from 'node:path';

if (typeof fs.glob !== 'function') {
  fs.glob = async function* (pattern, options = {}) {
    if (pattern !== '*.ts') throw new Error('fs.glob polyfill supports only *.ts');
    const cwd = options.cwd || process.cwd();
    const entries = await fs.readdir(cwd, { withFileTypes: true });
    for (const entry of entries) {
      if (entry.isFile() && entry.name.endsWith('.ts')) {
        yield entry;
      }
    }
  };
}
