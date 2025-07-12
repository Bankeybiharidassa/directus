export default function register({ init }) {
  init('routes', ({ app }) => {
    app.get('/core/frontpage', (_req, res) => {
      res.type('html').send('<h1>Nucleus Portal</h1><p>Welcome to Nucleus.</p>');
    });
  });
}
