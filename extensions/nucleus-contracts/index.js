const contracts = [{ id: 1, name: 'Sample Contract' }];

export default function register({ init }) {
  init('routes', ({ app }) => {
    app.get('/contracts', (_req, res) => {
      res.json(contracts);
    });

    app.post('/contracts', (req, res) => {
      const { name } = req.body ?? {};
      if (!name) {
        return res.status(400).json({ error: 'name required' });
      }
      const id = contracts.length + 1;
      contracts.push({ id, name });
      res.json({ id, name });
    });
  });
}
