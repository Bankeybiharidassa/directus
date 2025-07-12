export default function register({ init }) {
  init('routes', ({ app }) => {
    app.get('/support/ping', (_req, res) => {
      res.json({ pong: true });
    });
  });
}
