import fs from 'fs';
import path from 'path';

export default function register({ init, services }) {
  const { logger } = services;
  logger.info('Nucleus Core extension loaded');

  init('routes', ({ app }) => {
    app.get('/core/log/export', (_req, res) => {
      const logPath = path.join(process.cwd(), 'logs', 'directus.log');
      if (fs.existsSync(logPath)) {
        res.type('text/plain').send(fs.readFileSync(logPath, 'utf8'));
      } else {
        res.status(404).json({ error: 'log not found' });
      }
    });

    app.post('/core/config/reload', (_req, res) => {
      logger.info('Reloading Directus config');
      res.json({ status: 'reloaded' });
    });
  });
}
