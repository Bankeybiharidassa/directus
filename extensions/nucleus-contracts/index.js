export default function register({ init }) {
  init('routes', ({ app }) => {
    app.get('/contracts', (_req, res) => {
      res.json([{ id: 1, name: 'Sample Contract' }]);
    });
  });
}
