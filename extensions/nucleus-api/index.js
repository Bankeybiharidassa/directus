export default function register({ init }) {
  init('routes', ({ app }) => {
    app.get('/api/ping', (_req, res) => {
      res.json({ pong: true });
    });

    app.post('/api/assets/sync', (_req, res) => {
      res.json({ status: 'sync-started' });
    });

    app.post('/api/remote/control', (_req, res) => {
      res.json({ status: 'connected' });
    });
  });
}
