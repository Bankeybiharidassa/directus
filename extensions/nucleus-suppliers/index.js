const suppliers = [];

export default function register({ init }) {
  init('routes', ({ app }) => {
    app.get('/suppliers', (_req, res) => {
      res.json(suppliers);
    });

    app.post('/suppliers', (req, res) => {
      const { name } = req.body ?? {};
      if (!name) {
        return res.status(400).json({ error: 'name required' });
      }
      const id = suppliers.length + 1;
      suppliers.push({ id, name });
      res.json({ id, name });
    });
  });
}
