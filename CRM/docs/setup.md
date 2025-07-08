# Setup Guide

This repository provides a modular Directus instance with custom extensions.

## Installation

1. Copy `.env.example` to `.env` and fill in the required values.
2. Run `scripts/install.sh` to install Directus and enable the extensions.
3. Start the application with `npx directus start directus-app`.

All installation logs are written to `/var/log/nucleus/install.log`.

## Local testing

For development or automated GUI checks, use `./test_install.sh` instead of
`install.sh`. This helper script installs Python and Node dependencies in a
virtual environment and launches the backend and auth services on
`localhost`. Service output is stored in `/var/log/nucleus/test_install.log`.
After it finishes you can browse to `http://127.0.0.1:8000/core/login` or run
`node scripts/headless_check.js` and `scripts/gui_loop.sh`.
