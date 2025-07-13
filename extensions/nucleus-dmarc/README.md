# Nucleus DMARC Extension

Contains simple endpoints for DMARC report handling. `GET /dmarc/report` lists submitted reports and `POST /dmarc/report` accepts a JSON body with `domain` and `data` fields to add a new report.
