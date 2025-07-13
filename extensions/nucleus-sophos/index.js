export default function register({ init }) {
  init('routes', ({ app }) => {
    const statuses = [
      { host: 'server1', status: 'protected' },
      { host: 'server2', status: 'outdated' },
    ];

    app.get('/sophos/status', (_req, res) => {
      res.json(statuses);
    });
  });
}
