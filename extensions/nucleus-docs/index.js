import PDFDocument from 'pdfkit';
import { stringify } from 'csv-stringify/sync';

export default function register({ init }) {
  init('routes', ({ app }) => {
    app.post('/docs/generate', async (req, res) => {
      const { type, data } = req.body ?? {};
      if (type === 'pdf') {
        const doc = new PDFDocument();
        const chunks = [];
        doc.on('data', (c) => chunks.push(c));
        doc.text(JSON.stringify(data, null, 2));
        doc.end();
        await new Promise((r) => doc.on('end', r));
        res.type('application/pdf').send(Buffer.concat(chunks));
      } else if (type === 'csv') {
        const csv = stringify(data || []);
        res.type('text/csv').send(csv);
      } else {
        res.status(400).json({ error: 'unknown type' });
      }
    });
  });
}
