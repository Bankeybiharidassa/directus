import imaps from 'imap-simple';
import { parseStringPromise } from 'xml2js';

export default function register({ schedule, services }) {
  const { logger } = services;
  schedule('0 * * * *', async () => {
    const config = {
      imap: {
        user: process.env.IMAP_USER,
        password: process.env.IMAP_PASSWORD,
        host: process.env.IMAP_HOST,
        port: 993,
        tls: true,
        authTimeout: 3000,
      },
    };
    try {
      const connection = await imaps.connect(config);
      await connection.openBox('INBOX');
      const results = await connection.search(['UNSEEN'], { bodies: [''] });
      for (const res of results) {
        const all = res.parts.find((p) => p.which === '');
        try {
          const parsed = await parseStringPromise(all.body);
          logger.info('Parsed XML email', parsed);
        } catch (err) {
          logger.error('Failed to parse email', err);
        }
      }
      await connection.end();
    } catch (err) {
      logger.error('IMAP connection error', err);
    }
  });
}
