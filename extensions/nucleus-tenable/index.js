export default function register({ init }) {
  init('routes', ({ app }) => {
    app.get('/tenable/assets', (_req, res) => {
      res.json([]);
    });
  });
}
