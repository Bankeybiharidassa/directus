export default function register({ init }) {
  init('routes', ({ app }) => {
    app.get('/dmarc/report', (_req, res) => {
      res.json({ records: [] });
    });
  });
}
