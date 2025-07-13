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

    app.get('/core/api/settings', (_req, res) => {
      res.json({ settings: { example: true } });
    });

    app.post('/core/bs-check', (_req, res) => {
      logger.info('Running BS-check');
      res.json({ status: 'running' });
    });

    app.post('/core/security-scan', (_req, res) => {
      logger.info('Security scan started');
      res.json({ status: 'started' });
    });

    app.post('/core/cert/request', (req, res) => {
      const { hosts } = req.body ?? {};
      if (!hosts) {
        return res.status(400).json({ error: 'hosts required' });
      }
      logger.info('Certificate request', hosts);
      res.json({ status: 'requested', hosts });
    });
  });
}
