const reports = [];

export default function register({ init }) {
  init('routes', ({ app }) => {
    app.get('/dmarc/report', (_req, res) => {
      res.json({ records: reports });
    });

    app.post('/dmarc/report', (req, res) => {
      const { domain, data } = req.body ?? {};
      if (!domain || !data) {
        return res.status(400).json({ error: 'domain and data required' });
      }
      const entry = { domain, data, id: reports.length + 1 };
      reports.push(entry);
      res.json(entry);
    });
  });
}
