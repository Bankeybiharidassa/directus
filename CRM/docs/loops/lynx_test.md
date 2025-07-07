# Lynx test procedure

Run `./test_install.sh` to start the backend and auth services locally. This script installs Python and Node dependencies, launches the servers on localhost, and waits for ports 8000 and 3001 to respond.
Do not run `install.sh` or `scripts/patch_services.sh` in the Codex environment; they are production only.
Ensure `fpdf2` and `psutil` are installed in the Python environment before running tests.

Once running, open `lynx http://127.0.0.1:8000/core/login` and navigate through all pages for each role. Record the output in `logs/lynx_test-<role>.log`.
After completing the TUI visit, run `node scripts/headless_check.js` to capture screenshots and exported menu items. The headless script stores results as `logs/<role>_dashboard.png` and `logs/browser_<role>.json`.
Alternatively run `scripts/gui_loop.sh` to automate the entire process, including saving `lynx` dumps for each role.
