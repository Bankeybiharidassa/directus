# DEPLOYMENT

Volg deze stappen om Nucleus in productie uit te rollen:

1. Vul alle variabelen in `config/.env.template` en plaats het resultaat als `.env` op de server.
2. Draai `./scripts/install.sh` om alle dependencies te installeren en de database te initialiseren.
3. De installer plaatst systemd units `nucleus-backend.service` en `nucleus-auth.service`.
   Deze zijn meteen actief. Gebruik `scripts/manage_services.sh status` om de status te controleren.
4. Controleer de audit logs in `logs/` en zorg voor periodieke backups van de database.

Updates worden uitgerold via standaard CI/CD met een volledige test- en OTAP-ronde.
