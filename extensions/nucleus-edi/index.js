import { parseStringPromise } from 'xml2js';

export default function register({ init, services }) {
  const { logger } = services;
  init('routes', ({ app }) => {
    app.post('/edi/parse', async (req, res) => {
      try {
        const json = await parseStringPromise(req.body);
        logger.info('Received EDI', json);
        res.json(json);
      } catch (err) {
        logger.error('EDI parse error', err);
        res.status(400).json({ error: 'invalid xml' });
      }
    });
  });
}
