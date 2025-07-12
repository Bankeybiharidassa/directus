export default function register({ init }) {
  init('routes', ({ app }) => {
    app.get('/crm/info', (_req, res) => {
      res.json({ status: 'ok' });
    });
  });
}
