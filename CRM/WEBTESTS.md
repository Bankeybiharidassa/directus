# Web Tests

Dit document geeft een samenvatting van de handmatige lynx-tests.

## Uitgevoerde stappen
- Backend gestart via `python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000`
- Node-auth service gestart via `node node_backend/index.js`
- Pagina's bezocht met `lynx`:
  - `/core/login`
  - `/core/frontpage`
  - `/core/login?role=admin`
  - `/core/admin`
  - `/core/status`
- Testgebruiker aangemaakt via de auth API en succesvol ingelogd.

Logs zijn opgeslagen in `logs/codex_gui_loop_admin_20250705.log` en de volledige testuitvoer in `logs/codex_loop_run_20250705-1117.log`.
