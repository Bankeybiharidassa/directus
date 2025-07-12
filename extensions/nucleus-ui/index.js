export default function register({ init }) {
  init('routes', ({ app }) => {
    app.get('/core/theme.css', (_req, res) => {
      res.type('text/css').send(':root { }');
    });
  });
}
