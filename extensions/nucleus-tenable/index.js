const assets = [
  { id: 1, hostname: 'server1', status: 'healthy' },
  { id: 2, hostname: 'server2', status: 'warning' },
];

export default function register({ init }) {
  init('routes', ({ app }) => {
    app.get('/tenable/assets', (_req, res) => {
      res.json(assets);
    });
  });
}
