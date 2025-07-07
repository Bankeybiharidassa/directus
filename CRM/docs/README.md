# README.md — OpenAI Codex Bridge Client (C++ GUI + Python Backend)

**Project Summary**

Dit platform biedt een volledig lokaal bridge-client voor veilige interactie met OpenAI API's via een native C++ GUI en Python backend.

**Designregels**
- Elke CLI-functie moet ook via GUI toegankelijk zijn
- Standaard integratie van closed-loop testen
- Temperatuur altijd op 0.0 tenzij overschreven
- OTAP-strict development lifecycle
- Volledige ISO 27001 en NIS2 governance

**Modules**
- G1: Authenticatie en RBAC
- G2: CRM & Relatiebeheer
- G3: Logging, Mail, Config
- G4.x: CMS, Portal, Cases, Documentgenerator
- G4.5: Tenable integratie voor asset scans
- G4.6: DMARC analyser en rapportage
- CRM domeinbeheer voor DMARC
- Core: Logging, Build-integriteit, Closed Loops

**Security by Design**: MFA, IP whitelisting, certificaten (Let's Encrypt), YubiKey, encryptie op rust.

Zie ook [USAGE.md](USAGE.md) voor CLI- en GUI-voorbeelden.
Het volledige CRM API-overzicht staat in [CRM_API.md](CRM_API.md).
Een publieke landingpage is bereikbaar via `/core/frontpage`. De supportportal biedt tickets en een knowledgebase via de pagina `SupportHome`.
Voor productie-updates gebruik je `update.py` in twee stappen. Eerst
`update.py stage <repo>` om een testbuild te maken en alle tests uit te
voeren. Na goedkeuring kun je met `update.py deploy` de geaccepteerde
versie live zetten. Er worden automatisch twee backups bijgehouden en
`update.py rollback` kan de laatste versie herstellen.
