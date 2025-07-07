# Tenable Integratie

Dit project bevat een eenvoudige koppeling met Tenable.io/sc waarmee assets
en kwetsbaarheden gesynchroniseerd kunnen worden. De integratie is beschikbaar
op elk niveau (distributeur, partner, eindgebruiker en Nucleus zelf).

## API Keys

Voeg de volgende variabelen toe aan je omgeving of `config/settings.yaml`:

- `TENABLE_URL` – API-endpoint van Tenable
- `TENABLE_TOKEN` – toegangs-token

## CLI

```bash
python scripts/tenable_sync.py
```

## API

`GET /tenable/assets` — retourneert de lijst van assets uit Tenable.
