export default function register({ init }) {
  init('routes', ({ app }) => {
    app.get('/sophos/status', (_req, res) => {
      res.json({ ok: true });
    });
  });
}
