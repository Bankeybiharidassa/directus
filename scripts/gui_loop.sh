#!/bin/bash
# Start backend and auth services then run headless and lynx tests
./scripts/install.sh
node scripts/headless_check.js
# placeholder for lynx loops
