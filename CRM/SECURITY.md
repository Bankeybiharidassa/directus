# SECURITY

Deze applicatie vereist een harde security configuratie:

- MFA is verplicht voor alle gebruikers. Configureer TOTP of YubiKey in de GUI of via `nucleus user enforce-mfa`.
- Gebruik enkel sterk versleutelde verbindingen en plaats de backend achter een reverse proxy met TLS.
- Vul `config/.env.template` met productie-wachtwoorden en tokens en bewaar dit bestand buiten versiebeheer.
- Beheer IP-whitelist regels via `nucleus ip whitelist` of de GUI om toegang te beperken.
- Alle logbestanden bevinden zich in `logs/` en dienen periodiek gecontroleerd te worden.

Rapporteer kwetsbaarheden via het standaard responsible disclosure proces.
