export default function register({ init }) {
  init('routes', ({ app }) => {
    app.get('/core/theme.css', (_req, res) => {
      const primary = process.env.THEME_PRIMARY ?? '#0070f3';
      const background = process.env.THEME_BG ?? '#ffffff';
      const css = `
        :root {
          --primary-color: ${primary};
          --bg-color: ${background};
        }
        body { background-color: var(--bg-color); }
        button { background-color: var(--primary-color); color: #fff; }
      `;
      res.type('text/css').send(css);
    });
  });
}
