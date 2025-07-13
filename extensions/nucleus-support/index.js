export default function register({ init }) {
  init('routes', ({ app }) => {
    app.get('/support/ping', (_req, res) => {
      res.json({ pong: true });
    });

    const tickets = [];
    app.get('/support/tickets', (_req, res) => {
      res.json(tickets);
    });

    app.post('/support/tickets', (req, res) => {
      const { subject, message } = req.body ?? {};
      if (!subject || !message) {
        return res.status(400).json({ error: 'subject and message required' });
      }
      const id = tickets.length + 1;
      const ticket = { id, subject, message };
      tickets.push(ticket);
      res.json(ticket);
    });

    const assets = [];
    app.get('/support/assets', (_req, res) => {
      res.json(assets);
    });

    app.post('/support/assets', (req, res) => {
      const { hostname } = req.body ?? {};
      if (!hostname) {
        return res.status(400).json({ error: 'hostname required' });
      }
      const id = assets.length + 1;
      const asset = { id, hostname };
      assets.push(asset);
      res.json(asset);
    });
  });
}
