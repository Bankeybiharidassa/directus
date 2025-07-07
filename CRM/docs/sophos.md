# Sophos Integratie

Dit project bevat een basiskoppeling met Sophos Central voor zowel partner- als klantomgevingen.

## Partner API
- OAuth2 `client_credentials` authenticatie.
- `PartnerAPI` klasse in `backend/services/sophos_partner.py` haalt een access token op en lijst tenants.
- Tokens worden in geheugen gecachet zodat herhaalde aanroepen geen nieuwe token vereisen.

## Customer/Tenant API
- `CustomerAPI` in `backend/services/sophos_customer.py` verkrijgt een tenant token via een refresh token.
- Met `fetch_alerts` kunnen per tenant de alerts worden opgehaald.

In de CRM-module is per klant het veld `sophos_api_mode` toegevoegd om aan te geven of de Partner- of Customer-workflow wordt gebruikt.

Alle verzoeken worden gelogd naar `/var/log/nucleus/sophos.log`. Zie de tests in `tests/test_sophos.py` voor voorbeeldgebruik.
Na een update kan deze logbestemming onbeschrijfbaar worden. Draai in dat geval
`sudo ./scripts/set_permissions.sh /opt/nucleus-platform/CRM nucleus` om de correcte
rechten te herstellen.
