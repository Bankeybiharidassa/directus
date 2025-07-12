export default function register({ init }) {
  init('routes', ({ app }) => {
    app.get('/api/ping', (_req, res) => {
      res.json({ pong: true });
    });
  });
}
