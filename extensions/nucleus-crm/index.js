export default function register({ init }) {
  init('routes', ({ app }) => {
    app.get('/crm/info', (_req, res) => {
      res.json({ status: 'ok' });
    });

    const customers = [{ id: 1, name: 'Example Corp' }];
    app.get('/crm/customers', (_req, res) => {
      res.json(customers);
    });

    app.post('/crm/customers', (req, res) => {
      const { name } = req.body ?? {};
      if (!name) {
        return res.status(400).json({ error: 'name required' });
      }
      const id = customers.length + 1;
      customers.push({ id, name });
      res.json({ id, name });
    });
  });
}
