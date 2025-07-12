const fs = require('fs');
const path = require('path');

const baseDir = __dirname;

function checkDir(dirName, parent = '') {
  const full = path.join(baseDir, parent, dirName);
  const hasIndex = fs.existsSync(path.join(full, 'index.js'));
  const hasPackage = fs.existsSync(path.join(full, 'package.json'));
  console.log(`${parent}${dirName}: index.js ${hasIndex ? '✔' : '✖'} package.json ${hasPackage ? '✔' : '✖'}`);
}

for (const entry of fs.readdirSync(baseDir, { withFileTypes: true })) {
  if (!entry.isDirectory()) continue;
  if (entry.name === 'auth') {
    for (const sub of fs.readdirSync(path.join(baseDir, 'auth'), { withFileTypes: true })) {
      if (sub.isDirectory()) checkDir(sub.name, 'auth/');
    }
  } else {
    checkDir(entry.name);
  }
}
