Directus CRM Extension Audit Report
Findings
Extension Overview: The fork includes numerous custom extensions under /extensions, each intended to implement a CRM feature outlined in CRM/README.md. Key extensions (and their purposes) include: auth/keycloak (Keycloak OAuth2 login), nucleus-auth (generic OAuth2 flow), nucleus-crm (customer listing), nucleus-contracts (contract create/terminate), nucleus-docs (PDF/CSV generator), nucleus-edi (EDI XML parsing), nucleus-support (tickets & assets), nucleus-mail-ingest (IMAP email polling), nucleus-portal (public frontpage), nucleus-core (logging & maintenance API), nucleus-api (asset sync & remote control), nucleus-dmarc (DMARC reports), nucleus-sophos (Sophos status), nucleus-tenable (Tenable assets), nucleus-suppliers (supplier registry), and nucleus-ui (theming CSS)
raw.githubusercontent.com
raw.githubusercontent.com
. These map to the CRM modules G1–G4.6 from the README (Auth, Customer/Partner management, Contracts, Document generation, CRM hierarchy/EDI, Support desk, Portal/CMS, Core kernel, Tenable integration, DMARC analyzer, plus Sophos integration and UI theme).
Stub Implementations: Many extensions are incomplete stubs or placeholders. Instead of integrating with the Directus database or services, they use in-memory lists and static data. For example, the Contracts extension stores contracts in an array and simply pushes new entries on POST /contracts
raw.githubusercontent.com
. It doesn’t persist data to the database, meaning contracts vanish on restart and lack proper schema (only an id and name in-memory). Similarly, CRM (Customers) uses an in-memory customers array and adds a name on POST /crm/customers
raw.githubusercontent.com
. Support tickets and assets are also just stored in arrays and returned via API calls
raw.githubusercontent.com
. Suppliers, DMARC reports, etc., follow the same pattern (e.g. suppliers stored in-memory
raw.githubusercontent.com
). This “0% BS” policy mentioned in the README is not actually met – these are clearly placeholder implementations rather than production-ready logic.
Missing Business Logic & Data Integration: The current extensions lack proper business logic and data modeling. None of the custom endpoints interact with Directus collections or the database – a critical flaw. Directus extensions have full access to backend services (e.g. the Items Service for database operations)
directus.io
, but the code doesn’t leverage that. For example, a real CRM would use collections (tables) for Customers, Partners, Distributors, etc., enforce relationships and hierarchy via foreign keys or filters, and use Directus’s permission system (RBAC) to control access. Instead, the stubbed CRM and Support modules ignore RBAC and simply return or mutate a global array. This means no actual data persistence, no relational integrity, and no use of Directus’s powerful data layer – essentially bypassing the Directus CMS and defeating its purpose.
Incomplete Feature Coverage: Several CRM features from the README are not fully implemented or missing:
Partner/Distributor Hierarchy: The README calls for a hierarchy (nucleus admins → distributors → partners → end-users) and ensuring this structure is reflected in all modules, API, and RBAC. The codebase, however, has no dedicated extension or logic for managing distributor/partner relationships or enforcing hierarchy in data. There is no module to “Manage distributors, partners and endusers” aside from the generic nucleus-crm customers list (which doesn’t differentiate roles)
raw.githubusercontent.com
. The nucleus-crm extension only handles a list of customers by name
raw.githubusercontent.com
, and nucleus-suppliers is a simple list of suppliers
raw.githubusercontent.com
 – but nothing addresses distributors or partners explicitly. The absence of a module or collections for Partners/Distributors is a clear gap.
Auth & RBAC: Keycloak integration is only partially done. The auth/keycloak extension overrides the Directus login method to exchange credentials for a Keycloak token
raw.githubusercontent.com
, but this uses the Resource Owner Password flow (direct username/password exchange) which is generally not recommended. It doesn’t handle user provisioning or JWT validation properly – it just attaches an access token and calls loginWithCredentials()
raw.githubusercontent.com
, assuming Directus will accept that token. Similarly, nucleus-auth registers an OAuth2 strategy with dummy verify logic (accepting a hardcoded “good” code as valid)
raw.githubusercontent.com
raw.githubusercontent.com
. It claims admins can configure OAuth2 in Settings and that a “Sign in with Nucleus” button is shown
raw.githubusercontent.com
, but the actual code doesn’t implement the full OAuth redirect flow or assure that Directus knows about this strategy beyond logging it. There’s no logic to synchronize roles from Keycloak or ensure Directus roles (administrator, etc.) are assigned properly (the code has a roleMapping stub that maps “admin” → “administrator” but never uses it in authentication flow
raw.githubusercontent.com
). Overall, SSO integration is incomplete and may not function without additional work.
Document Generator: The nucleus-docs extension is minimally functional. It does generate PDF or CSV output from posted JSON data using pdfkit and csv-stringify
raw.githubusercontent.com
. However, it simply dumps the JSON into a PDF as text, with no template or formatting. There is no interface to trigger document generation from the Directus app – it’s purely an API endpoint (POST /docs/generate). Features like template selection, downloading documents, or saving them to the Files library are not implemented. It’s a proof-of-concept rather than a full feature.
EDI Messaging: The nucleus-edi extension only provides a /edi/parse route that converts an XML string to JSON and logs it
raw.githubusercontent.com
. There’s no actual messaging workflow – no storage of EDI messages, no routing between distributors and partners, and no interface. It doesn’t fulfill the “EDI messaging between distributors and partners” beyond basic parsing.
Support Desk & Assets: The nucleus-support API supports creating/listing tickets and assets with minimal fields
raw.githubusercontent.com
, but there’s no connection to a frontend module. Users cannot view or manage tickets in the Directus UI; they would have to call the API. The expected features (“list view” of tickets/assets, tracking asset vulnerabilities, etc.) are absent. For instance, there’s no field for asset vulnerability status or integration with vulnerability feeds (though Tenable/Tenable extension might tie in, it currently doesn’t). Also, mail ingestion is not integrated with the ticket system – the Mail Ingest extension fetches unseen emails and parses XML bodies
raw.githubusercontent.com
, but after parsing, it just logs the result via logger.info
raw.githubusercontent.com
. The README says parsed messages are stored as tickets
raw.githubusercontent.com
, but in code they are not stored at all. So the email-to-ticket functionality is effectively unimplemented (the code doesn’t create a new ticket entry in the tickets array or anywhere).
CMS & Public Portal: The codebase does not include any content management extension beyond what Directus already provides. nucleus-portal simply returns a hardcoded HTML snippet for /core/frontpage
raw.githubusercontent.com
. There’s no mechanism to “Create and publish pages” via Directus – presumably the authors expected using Directus Collections for pages, but no such collection or custom interface is present. “Revoke portal access” (perhaps revoking end-user login to a support portal) is not implemented; nothing in the code handles user account status or portal permissions specifically.
Core Kernel Features: nucleus-core implements endpoints for log export, config reload, system check, security scan, and ACME cert request, but most are dummy. For example, GET /core/log/export likely tries to read the Directus log file (though it’s not shown how), POST /core/bs-check and /core/security-scan probably perform no real actions (just return success). The README indicates these should perform real checks (security scan, etc.), but the code appears skeletal. Similarly, POST /core/cert/request is supposed to handle ACME certificate requests – none of that is actually wired to an ACME client. These endpoints exist only in name
raw.githubusercontent.com
 without underlying logic.
Tenable & Sophos Integration: Both nucleus-tenable and nucleus-sophos return static example data (lists of hosts with statuses)
raw.githubusercontent.com
raw.githubusercontent.com
. There’s no actual API call to Tenable.io or Sophos Central. They serve as placeholders showing what data might look like. In practice, they neither fetch real vulnerability data nor store anything in the system. This falls short of “integration” – it’s hardcoded demo output.
DMARC Analyzer: nucleus-dmarc similarly just keeps a list of submitted reports in memory
raw.githubusercontent.com
. There’s no parsing of real emailed DMARC reports, no cron job to fetch them, and no aggregation of statistics per tenant or domain. It doesn’t meet the feature description aside from accepting and listing dummy data.
Lack of Directus App Extensions (UI): None of the extensions add new App Modules or Interfaces to the Directus Data Studio. Directus allows extensions to create new modules in the left navigation (for custom pages or dashboards)
directus.io
, but the repository contains no evidence of Vue components or module registration on the client side. For example, we would expect a “Support” module in the UI for helpdesk agents or a “CRM” module for sales reps – but currently, all extensions are back-end API only. One hint is in nucleus-mail-ingest README: it says admins manage IMAP settings under “Support → Mail Ingest”
raw.githubusercontent.com
, implying a UI screen. However, no such admin interface code exists. Possibly, the authors intended to use Directus’s built-in collection forms (e.g. maybe they created a collection for mail settings or planned to but didn’t). In summary, the custom features are not surfaced in the Directus admin app at all, making them difficult to use for end-users. An extension is supposed to leverage UI components when needed
directus.io
 – here that part is largely missing.
Wiring and Packaging: All extensions are placed in the /extensions directory and export a register() function (or equivalent default) as required by Directus. This is correct in principle: Directus will auto-load these on startup. The extension names and grouping appear consistent (the pnpm-workspace.yaml includes extensions/*, meaning each has its own package)
raw.githubusercontent.com
. However, there might be a minor naming issue: the Keycloak extension’s default export function is named registerKeycloakAuth in code
raw.githubusercontent.com
. While it’s still the default export, using a non-standard name might be confusing. In general though, these are recognized by Directus – for instance, the nucleus-ui extension successfully registers a route to serve a dynamic CSS, and one can fetch /core/theme.css to get theme colors from env vars
raw.githubusercontent.com
. So the basic wiring is functional: the backend loads the routes, scheduled jobs, and auth overrides defined by these extensions. The gaps are in completeness and integration, not the loading mechanism.
Test Coverage & CI: The project’s test setup is not robust. The monorepo has Vitest configured (vitest appears in devDependencies and the root script uses pnpm run test to run package tests
raw.githubusercontent.com
), but there are no actual unit tests for the new extensions. We did not find any .spec.ts/.test.js files alongside the extension code, nor references to testing logic. As a result, it’s likely that running pnpm run test executes Directus’s core tests (if any) and possibly tries to run tests in each extension package (which have none, thus immediately succeeding). However, the mention of a CI failure with exit code 129 suggests something is hanging or crashing. A likely culprit is the scheduled IMAP job in nucleus-mail-ingest. That extension uses a cron schedule to poll email every hour
raw.githubusercontent.com
. In a test or CI environment, if the scheduler is active, it might not allow the process to exit, or could throw an error due to missing IMAP credentials. Exit code 129 corresponds to a fatal signal (128 + 1, perhaps SIGHUP or SIGINT) often indicating the process was killed due to a hang. This implies CI might be stuck running (Vitest not exiting) because of open handles like the cron job or perhaps an unhandled promise. Additionally, without proper teardown, the Passport strategy or open network calls could cause issues. In short, the test configuration is either misconfigured or the extensions are not test-friendly:
No mocks for external services (IMAP, Keycloak, etc.) are in place.
Long-lived timers or cron jobs aren’t disabled during tests.
There is no evidence of integration tests for the new API endpoints (e.g., no automated check that POST /contracts actually terminates a contract).
This all results in poor CI reliability. The Vitest setup (likely using a root vitest.config or default) wasn’t adjusted to accommodate the new extensions, so the project is not enforcing quality via tests. The presence of Vitest and a Vitest coverage plugin in package.json
raw.githubusercontent.com
 is moot since nothing targets these new modules.
Quality of Setup: The repository shows signs of incomplete integration work. The documentation (CRM README) is ambitious, but the implementation lags behind. Even basic features like storing data use trivial approaches rather than utilizing Directus’s framework. No migration or schema files are provided for new collections (which implies if one sets up this system, none of the CRM-specific tables exist – everything would have to be created on the fly in memory or manually). The Continuous Integration (CI) likely fails (as indicated) or doesn’t actually validate the CRM functionality. The extensions themselves do log some messages (for instance, nucleus-auth writes to logs/auth_init.log on load
raw.githubusercontent.com
, nucleus-core logs a startup message
raw.githubusercontent.com
), meaning the developers had debugging in mind. But beyond logging and basic route stubs, the extensions are not production-ready. In summary, each required feature is only partially realized: the skeleton is present, but the meat is missing.
Complete TODOs for Full CRM Functionality
To transform this codebase into a fully functional, CRM-compliant system as per the design, extensive work is required for each module. Below is a comprehensive TODO list:
General Data Modeling: Define proper Directus collections for all core CRM entities. At minimum, create collections (with appropriate fields and relations) for:
Distributors, Partners, End Users, and Customers: reflecting the hierarchical CRM & partner structure. Include relations (e.g. each Partner has a reference to its Distributor, each End User references its Partner or Distributor). This addresses G4.2’s hierarchy requirement.
Suppliers: with relevant info (name, contact, etc.). Possibly link Suppliers to Distributors/Partners if needed.
Contracts: including fields like contract name, status, start/end dates, associated customer/partner, etc.
Tickets (Support Desk): fields for subject, description, status, priority, linked customer or asset, etc.
Assets: fields for hostname, asset details, owner (customer/partner), vulnerability status, etc.
Pages/Posts (CMS): if implementing a portal CMS, a collection for portal pages or knowledge base articles, with fields like title, content, publish status.
Mail Ingest Settings: possibly a collection to store IMAP configuration, if we want admins to update it via UI rather than only .env.
DMARC Reports: a collection to store parsed DMARC report data (e.g. domain, date, aggregate results).
Tenable Findings / Vulnerabilities: collections for vulnerability data if pulling from Tenable (assets and their issues).
These collections should be added via Directus migrations or manual setup, and the extensions must use them instead of in-memory arrays.
Auth & SSO (Keycloak Integration):
Implement a proper OAuth2/OIDC login flow for Keycloak. Instead of using the password grant (which is currently hardcoded), use the authorization code flow:
Provide a route (or utilize Directus’s auth mechanisms) to redirect users to Keycloak’s authorization endpoint.
Handle the callback in Directus: exchange the code for a token (using NUCLEUS_CLIENT_ID/SECRET and Keycloak URLs from env). The nucleus-auth extension can handle this exchange properly (currently exchangeToken is a dummy that only accepts "good" code
raw.githubusercontent.com
 – replace this with real token exchange logic using Keycloak’s API).
Verify the token (JWT) using Keycloak’s public key or introspection. Extract user info and roles.
Provision or synchronize the user in Directus: If the user logging in via Keycloak doesn’t exist in Directus, create a new Directus user on-the-fly (assigning a role based on Keycloak role claims or a default). For example, map Keycloak roles to Directus roles (the roleMapping object
raw.githubusercontent.com
 should be utilized to translate external roles like “admin” to a Directus role slug).
Adjust the Directus login page UI to show a “Login with Keycloak” button properly. This might involve using Directus’s environment config (e.g. setting AUTH_OPENID_ENABLED=true and related OIDC settings) or creating a small custom interface extension that inserts a button. The text in the README suggests a button is shown
raw.githubusercontent.com
 – implement that via the official method (Directus has an “Auth Provider” in settings: ensure the extension registers itself so the admin UI reflects it).
Ensure logout and token refresh flows are handled (possibly beyond initial scope, but needed for completeness).
Test the SSO: Confirm that one can log in via Keycloak and be redirected into Directus, with appropriate permissions. No placeholder logic should remain – use actual Keycloak endpoints and handle errors (incorrect credentials, etc. with user-friendly messages).
RBAC & Role Hierarchy:
Define Directus Roles for each user type: e.g. Nucleus Admin, Distributor, Partner, EndUser, SupportAgent, etc., as described. These roles should be created in the system with appropriate permissions on collections.
Implement logic to enforce the hierarchy. For example, when a Partner user logs in, they should only see their own End Users’ data, not other partners’. Directus can enforce this with role-based permissions (filtering collections by an assigned distributor/partner field). But some dynamic logic might be needed:
Possibly use collection-level hooks (an “API extension” hook) to filter queries. For instance, on fetching Customers collection, if the user is a Partner, modify the query to only return customers under that partner.
Alternatively, use Directus permission filters in the role settings (preferred if static rules suffice).
Provide an interface or at least documentation to manage role assignments for users (the default Users module can be used, just ensure it has fields for linking a user to a Partner or Distributor entity if needed for context).
Ensure that creating new records via API or UI automatically links them appropriately: e.g., if a Partner creates a new EndUser (customer), a hook could auto-set the EndUser’s parent_partner field to that partner’s id (to enforce hierarchy).
No stub logic here – the roles and relationships must be operational so that data segmentation and security is robust.
Customers/Partners/Distributors Module:
Implement a CRM Module in the Directus app UI for managing organizations and contacts. This could be as simple as enabling the standard Collections in the Content module (if you configure Directus collections properly, the built-in content manager might suffice). However, a custom Module Extension could provide a tailored UI:
For example, a module that shows a dashboard of KPIs (number of distributors, partners, customers) and provides easy navigation to each type.
Include forms or pages to create/edit Distributors, Partners, etc., possibly with a nested view of hierarchy (e.g. selecting a Distributor shows its Partners and their EndUsers).
At minimum, ensure the navigation menu has entries (via the Module extension or collection grouping) for these CRM entities so that admin users can manage them without using raw API calls.
Hook up the nucleus-crm API to these collections. The /crm/customers endpoint currently just lists a dummy array
raw.githubusercontent.com
. Instead:
Make it query the Customers collection in the database (using Directus Items service or an SQL query). Return real customer data (maybe with filters based on the requester’s role).
Support query parameters (pagination, filtering by name, etc.) if needed, or consider deprecating this custom endpoint in favor of using the core Directus items API. (Given Directus already provides an API for collections, a custom endpoint is only needed if complex logic is required.)
The POST /crm/customers should create a new customer record in the DB (and possibly assign it to the current user’s partner automatically).
Remove any hard-coded sample data from nucleus-crm once the DB integration is in place. No more { status: 'ok' } health-check unless needed (if a health check is needed, ensure it checks something meaningful, like DB connectivity or a count of records).
Contract Management:
Implement a Contracts collection with appropriate fields (unique ID, name/description, linked customer or partner, status, start date, end date, etc.). Possibly include a relational link to a file (for contract documents) if needed.
Change nucleus-contracts to use this collection:
GET /contracts: fetch from the DB all contracts (with filtering by the user’s scope – e.g. a partner sees only their contracts).
POST /contracts: validate the input (e.g. require a name and associated customer/partner), create a new contract record in the DB (using Directus Items service).
POST /contracts/:id/terminate: update the contract’s status field in the DB to “terminated” (and maybe set an end date). Currently it just marks an in-memory object
raw.githubusercontent.com
 – replace that with an actual update query.
Add logic as needed: if termination requires certain conditions (maybe can only terminate active contracts, etc.), enforce that.
On the front-end, allow users to manage contracts. This could be via the standard content UI (just enable the Contracts collection), or a custom page in a CRM module where, for example, an admin can click “Terminate” next to a contract and the extension’s API is called.
Remove the in-memory contracts array
raw.githubusercontent.com
 and any placeholder contract. All operations should rely on persistent data.
Document Generator (Docs):
Expand the nucleus-docs functionality:
Introduce templates or at least different document types. For example, allow generating a PDF contract summary, or a CSV of customers. This could be done by interpreting the type or an additional parameter.
If possible, integrate with a library to generate richer PDFs (currently it just prints JSON text
raw.githubusercontent.com
). Define a format – e.g., for a “contract” type, generate a nicely formatted PDF with contract details and perhaps a signature line.
Implement security: only authorized users should be able to generate certain documents (check user roles or require authentication on the /docs/generate route – Directus should handle auth on extensions routes by default, but ensure the route is behind the auth middleware).
Consider saving generated documents: for instance, when a PDF is generated, you might store it in Directus Files (using the Files Service) so that it can be accessed later via the Directus file library.
Create a UI action for this if needed. For example, a custom Button interface in Directus that triggers document generation for a given item (Directus has flows/operations; alternatively, a custom panel or interface could call the /docs/generate endpoint and download the file).
Ensure required Node libraries (pdfkit, etc.) are included and configured. The PDF generation currently uses pdfkit, which should be fine. The CSV uses csv-stringify which is included. Just make sure to handle large data or streaming if needed (pdfkit usage is okay as shown, but monitor memory for very large JSON).
Write tests for the docs endpoint: e.g., POST a sample payload and assert the PDF binary contains expected content.
CRM & Partner Structure (Hierarchy & EDI):
Enforce hierarchy across modules: After establishing the collections for distributors, partners, etc., update all relevant endpoints to respect that hierarchy. For example:
When listing customers (GET /crm/customers), if the requester is a Partner, only show customers under that partner. If they are a Distributor, show customers under their downstream partners, etc. This might be done via directus permission filters or via programmatic checks in the endpoint handlers.
Similarly, ensure the Support tickets and Assets are scoped (a partner should not see tickets belonging to another partner’s customers, for instance).
EDI Messaging: Develop the EDI messaging workflow:
Possibly create a collection for EDI messages or transactions. When nucleus-edi parses an incoming XML (likely representing an order or data exchange between a distributor and partner), store the parsed content in this collection or process it (e.g., create an Order record in a hypothetical Orders collection).
Implement responses or acknowledgments if needed. If EDI is meant to be two-way, there should be an endpoint to send or simulate sending EDI messages to partners. Consider adding POST /edi/send to format JSON to EDI XML or another required format.
Remove the simple logger.info and ensure that parsed data is actually saved or used. Perhaps integrate with the Document Generator to output EDI in a user-friendly way, or create notifications on receiving new EDI messages.
This part might require clarifying the specific EDI use-case, but at minimum make it more than just parse-and-forget.
Add error handling for malformed XML, and security checks (only allow authorized integration accounts to post raw EDI).
UI for Hierarchy: If not using default collection view, create a UI view where an admin can visualize the hierarchy (e.g., a tree view of Distributors → Partners → Customers). This could be a custom Module or even just documentation on how to filter in the content module. But for user-friendliness, a tree or nested list module extension would be ideal.
Support Desk Module (Tickets & Assets):
Persist tickets and assets: Replace the in-memory tickets and assets arrays
raw.githubusercontent.com
 with actual collections Support_Tickets and Support_Assets. Define fields:
Tickets: subject, message (description), status (open/closed), priority, created_by (user who created ticket), assigned_to (support agent), related customer or partner, timestamps, etc.
Assets: hostname, description, owner (link to a customer or partner), vulnerabilities (perhaps a JSON field or relation to a Vulnerabilities collection if pulling from Tenable), etc.
Update nucleus-support endpoints:
GET /support/tickets: query the tickets collection (filter by current user’s scope: e.g., a partner sees only their org’s tickets, a support agent might see all or assigned ones).
POST /support/tickets: create a new ticket in the DB. Include logic to set default status, maybe assign it to a support team queue. Use the request body fields properly (subject/message required as before
raw.githubusercontent.com
, but also allow optional fields like priority or attachments).
GET /support/assets: fetch assets from DB (again scope by user if necessary).
POST /support/assets: create a new asset in DB (validate hostname as before
raw.githubusercontent.com
, and possibly tie it to the current user’s organization).
Possibly add new endpoints:
PATCH /support/tickets/:id to update status (e.g. close a ticket).
GET /support/tickets/:id for detailed view (or rely on Directus core API for that).
Mail Ingest Integration: Modify nucleus-mail-ingest:
After parsing an email’s XML (which presumably might contain a ticket description or some structured info), create a Support_Tickets entry from it. For example, if the email subject is available, use it as ticket subject, and the XML content as the message (or attachment).
Mark emails as read or move them, to avoid re-processing on next poll.
Provide feedback in logs about how many tickets were created or updated.
Also, allow the scheduling interval to be configurable (maybe via env it already is – currently it’s hard-coded to run hourly via cron
raw.githubusercontent.com
). Ensure that if IMAP credentials are missing or wrong, the error is caught (currently logs an error
raw.githubusercontent.com
 but continues). Possibly implement a retry or backoff strategy for robustness.
Importantly, in test or dev mode, allow disabling this scheduler. For instance, set an env like MAIL_INGEST_DISABLE=true in test environment and have the extension check that to skip scheduling. This will prevent CI hangs due to a running cron job. Document this as well.
Support UI: Create a Support module in the Directus app:
A custom module could provide a tailored interface listing tickets and assets in a user-friendly way (perhaps with filters for status, search, etc.).
Alternatively, use Directus’s collections interface: ensure that the Tickets and Assets collections are visible and properly permissioned for relevant roles (partners might have read-only access to their tickets, support agents have full access, etc.).
If resources allow, implement convenience features like a dashboard panel showing number of open tickets, recent tickets, etc., using Directus Panels extension or a custom Insight.
Provide an interface for the Mail Ingest configuration if needed: e.g., a page under Support module where an admin can test the IMAP connection or see last run time. (This might be advanced; at minimum document how to configure via env and monitor via logs.)
CMS & Public Portal:
Determine how the portal is meant to function. The README hints at a “Public landing page” at /core/frontpage and the ability to publish pages (possibly knowledge base or documentation pages for end-users).
Leverage Directus’s capabilities to manage content:
Create a Pages collection (if not already) for portal content or use Directus’s built-in “Pages” if this was a template. Fields might include title, slug, content (HTML/markdown), publication status, etc.
Extend nucleus-portal:
Instead of returning a hardcoded HTML snippet
raw.githubusercontent.com
, have it fetch and serve actual content from the database. For example, GET /core/frontpage could retrieve a page marked as the frontpage and return its HTML (or JSON to be rendered by a frontend).
Possibly implement a simple templating or use Directus’s public REST API for content. Since Directus is headless, another approach is to create a small frontend app for the portal. However, given constraints, one could use an Express route to serve a basic HTML that includes content from the DB.
Implement /core/login properly if needed (the README mentions an HTML login page for different roles). Ensure that page is served and the authentication (via Keycloak or local) works, then redirects to the correct role’s dashboard.
Implement “revoke portal access”: likely meaning the ability to disable a partner/end-user’s login to the portal. This could be done by deactivating their Directus user or removing a “portal access” role. Provide an easy way (maybe a toggle field on the user or the partner record) and ensure that if toggled off, that user cannot log in (Directus user status or a check in the auth flow).
Set up appropriate permissions for public vs. authenticated portal access. If certain pages are public (like a landing page) allow anonymous read on that content collection or serve it without auth. Other pages (like support portal with tickets) should require login.
On the Directus admin side, allow admins to create and edit portal pages through the Collections (Pages collection).
If needed, create a Portal theme or use the nucleus-ui extension to style the portal pages. The nucleus-ui currently injects CSS for primary and background color from env
raw.githubusercontent.com
. That can be extended to include more branding elements (logo, etc.) or use Directus’s theming system if applicable.
Essentially, turn the portal from a stub into a minimal functioning site:
Anonymous users see a landing page at /core/frontpage with info.
Authenticated end-users (customers) can log in (maybe via the same login page but with role-specific redirect) and see their tickets or assets.
Partners/distributors can log in and see their own dashboard (which might include customer lists, etc., as per README’s “Role dashboards provide customer lists, tickets and asset views for distributors, partners, end users, and company users” – that implies multiple dashboards).
It might be beyond Directus’s standard UI to have multiple dashboards – possibly the intent was to use the portal (React frontend) for that. However, since we aim to do it in Directus: an alternative is to use the Insights module with custom panels for each role’s dashboard. Or simpler, just provide filtered views: e.g., when a Partner logs into Directus, they go to the Content module filtered to their customers, etc. But to truly follow the spec, one might need to develop a custom front-end for the portal outside Directus. (Given the constraint “only contents of the forked repo may be used”, we focus on what can be done inside Directus).
Summary: The portal needs to allow page publishing and serve those pages, and manage user access – all of which currently is not implemented.
Core Kernel (Logging, Config, Checks, Security):
Flesh out nucleus-core endpoints:
Log Export (GET /core/log/export): Implement this to read the Directus log file(s) from disk and return them (as download or JSON). Directus typically logs to logs/ directory. Use fs to read the file (the code likely already attempts this in part). Ensure proper error handling and permission (only admins should use this).
Config Reload (POST /core/config/reload): If Directus supports reloading config (environment variables) at runtime, call that. Directus doesn’t natively re-read env on the fly, so this might need a custom approach. Perhaps it was intended to reload some cached settings in the CRM backend (not clear). If not feasible, consider removing or documenting it as no-op, or implementing partial reload (e.g., flush some cache or reinitialize something).
API Settings (GET /core/api/settings): The README says “return example API settings”
raw.githubusercontent.com
. This suggests it’s not implemented. Either implement it to return relevant configuration (like which integrations are enabled, etc.), or remove if not needed. If keeping, provide actual data (maybe gather env vars like IMAP host, Keycloak URL but in a safe way – perhaps just a summary of enabled modules).
Basic System Check (POST /core/bs-check): Implement a system health check. This could include:
Checking database connectivity.
Checking external services (Keycloak, IMAP, etc.) if configured.
Checking that required env variables are present.
Perhaps performing a quick security audit (like ensuring default admin password is changed, etc.).
Return a JSON object with results of these checks (and use proper status codes if something is critically wrong).
Security Scan (POST /core/security-scan): This could tie into known vulnerability scanners. If Tenable was integrated, perhaps trigger a Tenable scan via API. If not, maybe run a Node security audit (like npm audit) or a simple OWASP dependency check. If that’s too heavy, another approach is to at least scan the Directus permissions for common misconfigurations. Since the README specifically mentions a CLI security scan, it might be expected to call an external tool. If that’s out of scope, ensure this endpoint at least responds with a message that a scan started or is not implemented. But ideally, integrate with Tenable or another scanner if possible.
Certificate Request (POST /core/cert/request): Integrate an ACME client (like Let’s Encrypt via a library such as acme-client) to actually attempt a certificate issuance. This is complex because it requires domain ownership and probably DNS or HTTP challenges. Potentially, this feature might be too environment-specific to fully implement here. One could simulate it (call ACME staging environment to request a cert for a test domain). If implementing, allow configuration of domain and ACME directory URL via request body or env. Otherwise, at least ensure this endpoint does something logical (e.g., returns an error “Not configured” if no ACME details).
Logging and Monitoring: Ensure that all these core operations log their actions to the system logs (for auditing).
Note: Some of these tasks (security scan, ACME) go beyond typical Directus scope and might border on “external code.” Since the rules allow code directly copied into the repo, you can incorporate necessary Node libraries (ensuring license compatibility). Keep it self-contained.
Test all these endpoints. E.g., simulate log file presence, call log export and verify contents; call bs-check with a known bad config to see it reports an issue.
Tenable Integration (Vulnerabilities):
Replace nucleus-tenable static output
raw.githubusercontent.com
 with a real integration:
If possible, use Tenable’s API (Tenable.io or Tenable.sc) by incorporating their official SDK or raw API calls. This likely requires API keys or credentials (to be provided via environment variables, e.g., TENABLE_API_KEY, etc.).
Implement endpoints to fetch relevant data, e.g., GET /tenable/assets could retrieve a list of assets with their status from Tenable in real-time or from a cached store. Or fetch vulnerabilities for assets and return those.
Perhaps create a Tenable_Assets collection in Directus to store imported data (could be updated by a scheduled job or on-demand via an endpoint). That would allow linking with the internal Assets (support) or customers.
Ensure any long operations are handled asynchronously if needed (Tenable’s data could be large; maybe have a background sync with a status).
If full integration is too heavy, at least design it such that the data is not hardcoded. For example, allow an admin to upload a Tenable export file via Directus Files and then parse that to populate asset vulnerabilities. This could be a compromise to get real data in without live API calls.
Remove the placeholder array in code and any references to static “server1/server2”. After this, the extension should either provide real data or not exist at all (stubs are not acceptable).
Optional: Provide a UI panel or page to display vulnerability stats (e.g., number of assets healthy vs at-risk). This could be part of an Insights dashboard or in the Support module for assets.
Testing: If using live API, you might need to mock responses for tests. If parsing a file, include a sample in tests to validate the parser.
Sophos Central Integration:
Similar to Tenable, implement nucleus-sophos to fetch actual endpoint protection status from Sophos Central (if intended). Possibly:
Use Sophos Central’s APIs (with credentials from env).
Provide an endpoint /sophos/status that either proxies data from Sophos or retrieves from a local cache table.
The current static list
raw.githubusercontent.com
 should be removed. If real-time integration is complex, consider at least a scheduled sync that updates a Sophos_Devices collection with device status (online/offline, last seen, protected/unprotected, etc.).
This could tie into assets – e.g., match Sophos devices to our Assets by hostname or serial.
If Sophos integration is not critical or accessible, clearly mark it and perhaps simulate it by reading from a config or file so that it’s not just a hardcoded two-item list. But ideally, implement the real deal if possible.
Testing: similar approach, ensure not to call actual APIs in tests without a mock.
DMARC Analyzer:
Enhance nucleus-dmarc:
Implement parsing of DMARC XML reports. DMARC aggregate reports come as XML (often zipped). We can use xml2js (already used for mail ingest) to parse an uploaded report.
Consider adding an endpoint or extending POST /dmarc/report to accept XML file uploads (maybe via a multipart form or instruct users to use Directus File upload then send the file ID).
Once parsed, store the data in the DMARC Reports collection (domain, date range, counts of passes/fails, etc.). The current endpoint takes a JSON with domain and data
raw.githubusercontent.com
 – that’s not realistic input from real reports. Instead, you might have POST /dmarc/report accept raw XML or a file reference and handle it internally.
Provide a GET /dmarc/report/:id for detailed report data or just rely on Directus item read.
Possibly aggregate by domain: e.g., GET /dmarc/summary?domain=example.com to show overall compliance stats from reports.
Remove or replace any in-memory storage with actual DB entries.
Add a small UI element if useful: for instance, a panel on an admin dashboard showing how many reports were received and if any domains have issues.
Test with real DMARC sample data to ensure parsing is correct (and write unit tests for the parser function).
UI/UX Integration:
After implementing the above backend changes, focus on exposing these features in the Directus app so that end-users (admins, support agents, partners, etc.) can actually use them:
Directus Navigation: Use extension manifest or the Module extension capability to add new sections. For example, a “CRM” module that perhaps encapsulates Customers, Partners, etc., and a “Support” module for tickets. Directus modules allow specifying a route and providing a Vue component for the main page
directus.io
. If building custom Vue components is outside the scope, an alternative is to use Directus’s ability to show collections. We can also employ the existing modules (like Collections and Insights) and just configure them well. But since the requirement is “native Directus extensions… fully integrated and working from /extensions,” it implies we should use the official extension system for any custom UI.
Custom Interfaces/Panels: If certain data should be visualized in a special way (like a hierarchical tree or a chart), consider writing a Panel extension for Insights or a Layout/Interface extension. For instance, an interface that shows the hierarchy selection (for linking a customer to a partner).
Settings UI: Ensure that any environment configurations that admins might need to change are either documented or surfaced in the Directus Settings. Directus doesn’t directly allow editing env via UI, but for OAuth, it might list the provider configuration (client ID, etc.) in the admin settings if properly registered. The nucleus-auth README suggests that after installation, credentials can be configured under Settings → Auth Provider
raw.githubusercontent.com
. Verify this – it likely requires adding a config option or using Directus’s existing OIDC config UI. If it’s not auto, create a custom settings page (perhaps a simple module that reads/writes a config collection for these values).
Theme Integration: The nucleus-ui extension generates CSS from env. Make sure the Directus app actually loads this CSS. Possibly instruct users to include a <link> to /core/theme.css somewhere. If needed, extend nucleus-ui to inject the stylesheet into the app (maybe via an App Hook if available). Also consider adding more theming variables or reading from Directus settings if dynamic theming is desired.
User Experience: Provide meaningful feedback on actions. E.g., if using custom modules, show toast notifications on success or error (Directus SDK can do this). Ensure required fields have validations in the UI, etc.
No Fake Screens: Remove any dummy or placeholder screens. For example, if any extension currently adds a menu item that leads to a blank page (none known, but just in case), replace it with real content or remove it.
Testing & Quality Assurance:
Write comprehensive tests for each extension:
Unit test the internal logic (e.g., DMARC XML parser function, EDI parser, PDF generation function).
Integration test the endpoints using Directus’s testing utilities or an HTTP client. For example, start the Directus app (in test mode with an SQLite memory DB), and simulate requests:
Create a customer via the /crm/customers endpoint, ensure it’s in the DB and retrievable.
Test that unauthorized access is blocked (e.g., hitting /support/tickets as an anonymous user should 403).
Test role-based restrictions (create a partner user, log in as them, ensure they only see their stuff).
Test the OAuth flow: this might require simulating Keycloak – perhaps mock the fetch to Keycloak token endpoint to return a fixed token for a known user.
Test mail ingest in isolation: mock the IMAP connection (since we don’t want tests depending on a real mail server). You might abstract the imap-simple calls so they can be overridden with a dummy in tests. Alternatively, allow dependency injection or simply don’t run the schedule in tests (set NODE_ENV=test to skip scheduling).
Ensure that no background jobs or open handles prevent tests from exiting. This may involve adding a teardown step in tests to stop cron jobs (node-cron has a way to stop scheduled tasks).
Aim for high coverage on all new modules, especially critical business logic.
Fix CI issues: With proper tests and by handling the above concerns, the CI should no longer hang with exit code 129. Confirm by running tests locally and in CI – ensure the process exits cleanly. If any extension still causes a hang, adjust it. (For example, if Passport’s strategy or some event loop hanging, ensure to close it or use Vitest’s --detectOpenHandles to pinpoint the issue).
Vitest configuration: If needed, create a vitest.config.js to increase timeouts for slower integration tests or to include setup files (like polyfills or env setup). Ensure to stub out external calls (you don’t want tests trying to call real Tenable or Keycloak endpoints).
Continuous closed-loop QA: Adopt a loop of implementing a feature, running the tests (and possibly some manual testing in a running Directus instance), then fixing any issues. Repeat until all tests pass and the features work as expected when clicking through the app. This was emphasized in the README as “design → build → test → verify → rework until operator approval” (closed-loop QC).
Documentation & Cleanup:
Update each extension’s README to reflect the new reality (the current READMEs describe the simplified behavior, which will be outdated once features are fully implemented). Provide usage instructions where appropriate (e.g., how to configure Keycloak, how to run a security scan, etc.).
Remove any development artifacts (console logs, test code, etc.) from production code.
Consider versioning these extensions (update package.json versions from 0.1.0 to 1.0.0 once complete).
If any placeholder or unused extension remains (for example, if we decided not to integrate Sophos for now), remove it or clearly mark it as example/demo in both code and documentation to avoid confusion.
Lastly, do a full end-to-end test as a user: simulate setting up the system from scratch (per docs/setup.md if available), ensure enabling the extensions, create some sample data through the UI, and verify all promised features (contracts can be created and terminated with data persisted, support tickets flow from email to portal, etc.). This will confirm that the system is truly fully functional and CRM-compliant.
By addressing all the above, each extension will have proper functional logic, UI screens, workflows, and backend wiring as required. The system will no longer rely on any mock logic or placeholders – all features will be production-ready and integrated into Directus.
Codex Instruction for Completing and Integrating All Extensions
Goal: Convert the stub extensions into fully functional Directus extensions with complete logic, UI integration, and tests. Use an iterative, test-driven approach (closed-loop corrections) for each module to ensure quality and completeness. Step 1: Set Up Development & Testing Environment
Ensure you can run the Directus project locally and execute tests:
Install dependencies (pnpm install) and start a development instance of Directus with the extensions enabled. Set environment variables for all needed services (Keycloak, IMAP, etc.), using dummy values or test endpoints as needed.
Run pnpm run build to build all extensions and core. Then run pnpm run start (or docker-compose up if applicable) to have a running Directus instance.
Run pnpm run test to see the current test status. If tests hang (due to scheduled jobs), temporarily disable those jobs (you will implement a proper fix later). For now, note any immediate failures or hanging processes – this will guide where to apply fixes.
Step 2: Implement Data Persistence for CRM Entities
For each extension that currently uses in-memory data, refactor it to use Directus services and the database:
Create Directus Collections: Using either Directus CLI or schema files, define collections for Customers, Partners, Contracts, Tickets, Assets, etc. (as detailed in the TODOs above). Each collection should have an accompanying TypeScript interface (if using TS) or clearly defined fields. For relationships (e.g., a Customer has a partner_id field linking to Partners), set up those relations in the schema.
Use ItemsService: In the extension code, import Directus’s ItemsService (e.g., import { ItemsService } from 'directus';). Replace array operations with service calls:
const service = new ItemsService('<collection-name>', { schema: database.schema, accountability: context.accountability }); (Directus typically passes services or you can get database from the context).
Use await service.readMany(query) for GET handlers, and await service.createOne(payload) or createMany for POST handlers. This ensures data goes into the DB.
Remove any global arrays (e.g., contracts, tickets, etc.) – these will be obsolete.
Example: In nucleus-contracts, instead of contracts.push(...)
raw.githubusercontent.com
, do:
const service = new ItemsService('contracts', { schema, accountability });
const created = await service.createOne({ name });
return res.json(created);
Similarly, for GET, fetch from service with appropriate filters.
Test after each refactor: Write a quick unit test or use an API tool (like cURL or Postman) to hit the endpoint and ensure data is saved. For instance, POST a new contract and then GET it. If it appears in the Directus database (you can query via Directus API or DB), the persistence is working.
Repeat for nucleus-crm (customers list), nucleus-support (tickets/assets), nucleus-suppliers, nucleus-dmarc, etc. Each time, verify the endpoints now interact with the database. If any extension requires additional fields (e.g., terminate setting a status), update the collection schema to have that field and implement the logic (using service.updateOne(id, { status: 'terminated' })).
Step 3: Enforce Role-Based Access Control and Hierarchy
Now that data is in the database, ensure that the endpoints and Directus permissions enforce the CRM hierarchy and security:
Update Directus Role permissions via migration or admin UI: for each collection, set read/write filters based on roles. Example: Partners role can only read Customers where partner_id is their own. Distributors can read Customers of their child partners, etc. If complex, plan to implement programmatic checks in the endpoints as well.
Implement endpoint guards: Within endpoints, use the context.accountability (which contains the user’s role and ID) to filter data:
E.g., in GET /crm/customers, if context.accountability.role is 'Partner', add a filter partner_id = context.accountability.userId or use a pre-set filter from accountability.administer or permissions.
Directus might automatically filter ItemsService results if the Accountability scope is limited by permissions. Test this: log in as a non-admin and call the endpoint to see if it respects the permissions. If not, manually apply .accountability filters.
Write tests for a couple of scenarios: e.g., create a Partner user, create two customers (one for that partner, one for another), and ensure the Partner user’s token can only retrieve their own customer. Use Directus REST API or the extension endpoint (depending on how you expose it). Adjust the code until the behavior is correct.
Implement any hooks needed: For example, use a collection hook (Directus extensions type: hook) on the Users collection or on create of customers to automatically assign the right relations. If a Partner user creates a Customer via Directus standard UI, you might want a hook to set that customer’s partner_id to the user’s org. Outline such hooks and implement if necessary using init('items.create', ...) extension points.
Step 4: Expand Auth Extensions for Real OAuth2
Focus on auth/keycloak and nucleus-auth:
Keycloak (auth/keycloak): Instead of directly using Resource Owner Password:
Create a new endpoint in this extension or elsewhere to initiate login. For instance, app.get('/auth/keycloak') that redirects to Keycloak’s /authorize URL with proper client_id, redirect_uri, scope, etc.
Create a callback endpoint app.get('/auth/keycloak/callback') to handle Keycloak’s redirect with a code parameter. In this handler, exchange the code for tokens by calling Keycloak (fetch(baseUrl + '/token') with grant_type=authorization_code). Use real values from process.env (which admin can set).
Once you get access_token (and possibly an ID token), verify it. Keycloak’s JWT can be verified using its public key or by calling Keycloak’s userinfo endpoint. For simplicity, you might skip deep verification if you trust the connection (or use jsonwebtoken library to verify the token signature with Keycloak’s certs).
Extract the user identity (username or email) and roles from the token. Then:
If a Directus user with that identity exists, retrieve it.
If not, create a new Directus user (via UsersService) with a placeholder password and mark auth via external provider.
Assign the Directus role based on Keycloak role claim (use the mapping function to map Keycloak roles to one of Directus roles like administrator, etc.).
Generate a Directus auth token for this user (you can call Directus core login function or create a JWT that Directus accepts – possibly by inserting a row in directus_sessions. Another approach: use the Directus API: POST /auth/login with email/password won’t work for SSO, instead, set up an integration where the callback logs the user in server-side).
Directus v10 might allow custom auth via setting accountability.user on the context and returning some session cookie. Research if Directus has a hook for custom auth strategies.
Alternatively, consider using the passport strategy approach fully: directus’s core might pick up a passport strategy if properly registered (in nucleus-auth we did passport.use('nucleus-oauth', strategy)
raw.githubusercontent.com
). Check if Directus automatically uses passport strategies for login if the naming matches. If not, you may manually handle the session.
Finally, redirect the user to the Directus frontend with a valid session or token (for instance, generate a Directus static token or use an URL with the access_token).
Nucleus OAuth2 (nucleus-auth): Adapt this general extension to support any OAuth2 provider (maybe it’s a generic fallback used by Keycloak). Since Keycloak is the main one, you might merge functionality or ensure nucleus-auth is used to configure the provider in Directus settings.
Possibly use the verifyToken and exchangeToken functions properly: remove dummy checks (if token === 'validtoken')
raw.githubusercontent.com
 and actually verify JWTs or call introspection endpoints. Remove the hardcoded “good” code logic
raw.githubusercontent.com
 and implement real token exchange for whichever provider is configured (this might overlap with Keycloak steps).
Ensure that the login page in Directus shows a “Sign in with Nucleus” or a more specific “Sign in with Keycloak” button. This might require adding a config entry in Directus’s auth.providers or using an App Extension to inject a custom login interface. The simplest route: instruct admins to enable the OIDC login in the environment (Directus has some support for OAuth2 login via env variables as of v10 – for example, setting AUTH_OPENID_<something>). If that’s available, leverage it.
After these changes, test the whole login flow:
Start Directus, go to the login screen, click the SSO button, ensure you’re redirected to Keycloak (you might use a dummy Keycloak or an Identity Provider stub for testing).
Simulate the callback with a valid code, and verify that you end up logged into Directus as the correct user.
Write an automated test for the exchange function (you can mock the fetch to Keycloak token endpoint to return a known JWT for testing, then ensure verifyToken returns the expected user object).
Step 5: Integrate External Services (Email, Tenable, Sophos, DMARC)
Implement the integration logic for each external-facing extension:
Mail (IMAP) Integration: We already partially addressed storing parsed emails as tickets. Now refine it:
Use a robust IMAP library (imap-simple as included). Write error handling and possibly limit the runtime (so it doesn’t hang indefinitely).
Ensure the schedule is registered via schedule (as done)
raw.githubusercontent.com
. Provide a way to stop it during shutdown (maybe not easy with cron; but as long as process exits it should end).
For testing, abstract the email fetching logic so it can be mocked. E.g., have a function fetchEmailsAndCreateTickets() that you can call, which uses env or passed config. In tests, replace that function with a dummy that just calls a callback without real network.
After implementing, run the scheduler manually in dev to see if it creates tickets from an actual test email.
Tenable API: Use Node’s fetch or axios to call Tenable’s endpoints. You might need to page through assets or vulnerabilities.
If the data is large, consider storing results in a new collection Vulnerabilities. For now, implement a simple fetch of a few assets for demonstration (to meet “no mock data” rule).
Protect any API keys by using env variables. Document these in README (e.g., need TENABLE_API_KEY, TENABLE_API_URL).
Test by hitting /tenable/assets – if you don’t have a real account, consider using their API’s demo mode or at least ensure the code runs without crashing if no credentials (perhaps return a graceful error).
Sophos API: Similar approach. Possibly use the Sophos Central API (requires OAuth2 client credentials flow). If that’s too complex, as an interim, allow an admin to upload a JSON export of device statuses and parse that.
But aim for actual connectivity: client ID/secret from env, obtain an OAuth token from Sophos, then call “GET endpoints” or similar to list devices and statuses.
Fill a Devices collection or just return the data directly. Ensure to remove static output.
DMARC Parsing: Implement a parser for DMARC XML:
Possibly reuse logic from mail ingest if DMARC reports might come via email. Or allow uploading the XML via the directus file library and then run a script.
Use xml2js as already imported to parse the XML structure (it will produce a JS object). Extract relevant fields (domain, record count, percentages of passes/fails, etc.).
Save the parsed summary to the DMARC Reports collection.
You might want to also store the raw report (maybe link to the file or store the XML in a Text field for reference).
Write unit tests for the parser with sample DMARC XML (find a sample report and include it in test fixtures).
Verify and test external integrations carefully: Because actual API calls might not be available in a test environment, you’ll need to mock them:
For Tenable/Sophos, abstract the fetch calls into a helper function or service class. In tests, stub those methods to return predetermined data (simulate a few assets with statuses).
For DMARC, test the parsing function offline.
For IMAP, as mentioned, simulate fetching by stubbing imaps.connect to return a fake connection object in tests.
Step 6: Build Frontend (App Extensions) for New Modules
Now ensure that everything we did on the backend is user-accessible through the Directus UI:
Module Extensions: Use the Directus extension framework to scaffold modules for CRM and Support:
If not already present, create a directory like extensions/modules/crm-module or similar (the scaffolding tool create-directus-extension can generate a module template in Vue). Since you must stay within this repo, you can manually create a minimal module:
A package.json with type "module" and a script pointing to an index.js or index.tsx that registers the module.
The module should define a route (e.g., /crm) and a icon/label (like "CRM").
Create a basic Vue component that lists some info or simply redirects to the Collections page for Customers. (Directus’s UI architecture might allow programmatically navigating to an existing page. Alternatively, use the component to fetch data via the new endpoints and display it.)
Keep it simple: maybe the CRM module component just calls /crm/customers API and displays the list in a table with minimal styling, since building a full UI from scratch is time-consuming. Or even embed an <iframe> pointing to a Docs page or external if needed (not ideal, but consider time).
Do similar for Support: a module at /support that lists open tickets or has tabs for Tickets/Assets.
Ensure to import any needed UI components from Directus (the docs mention you can leverage existing components
directus.io
).
These modules should be registered in the index with registerModule({ … }) giving them a name and path.
Test in UI: Rebuild the app (pnpm run build should compile the module extensions into the bundle). Refresh the Directus admin and verify new menu items appear for CRM and Support. Click them to see if your component renders. At this point, likely the components are very bare-bones – improve as needed:
Add ability to click on an item to view details (maybe link to the standard item detail drawer by route).
For Support, maybe add a button “Create Ticket” that opens the Directus item creation for Support_Tickets (you can use router.push('/content/support_tickets') as a cheat to use the built-in UI).
The key is to ensure navigation flow is not broken and users have a way to use the features without relying on raw API calls or an external tool.
Custom Interfaces (if needed): If any field requires a special input (maybe a JSON editor for DMARC data, or a tree selector for selecting parent org), implement a custom Interface extension. The Directus docs show how to register an Interface extension (basically a Vue component for form field).
For example, a hierarchical select interface for choosing a distributor/partner in user creation could be useful. If this is too much, skip unless necessary.
Dashboard Panels: Consider adding Panels in Directus Insights for a quick overview:
e.g., a panel showing “Open Tickets by Priority” or “Total Customers” by partner. Panel extensions can be created, or you can possibly achieve some via Directus’s built-in SQL panels if the data is in collections. This is optional polish.
Theming: Ensure the nucleus-ui CSS actually affects the UI. Perhaps add to the module’s component a <style>@import url("/core/theme.css");</style> or configure Directus to load it globally (maybe via an environment variable for custom CSS).
Test changing the env colors and see if the UI updates (with EXTENSIONS_AUTO_RELOAD on, it should rebuild and apply new CSS).
Final UI Testing: Manually test the UI:
Log in as various roles (Admin, Distributor, Partner, etc.) and verify:
The left nav shows only what they should see (you might hide the CRM module for non-admin, etc., via role restrictions in module or UI logic).
A partner can go to Support module and see only their tickets, can create a ticket (use the directus content button or provide a form).
The CRM module shows relevant info or at least doesn’t error out.
The standard Content/Collections area can also be used as a fallback (make sure the collections have user-friendly names and fields configured, since many admins will just use those).
Adjust any UI labels, etc., to be clear (e.g., rename “Nucleus Auth” to something user-understandable in settings).
Step 7: Comprehensive Testing (Automated and Manual)
Now run the full test suite and address any issues:
Execute pnpm run test. All tests should pass. If any fail, debug promptly:
If an external integration test fails due to no credentials, use Vitest to skip those tests unless creds are provided (use test.skip or mock the network calls).
If any test hangs, look for open handles: likely the IMAP cron. To fix, you can conditionally schedule the job only if NODE_ENV !== 'test' or expose a method to stop it. For example, in mail-ingest, after registering the schedule, if in test mode, call job.stop() immediately. You might also utilize Vitest’s beforeAll/afterAll to intercept and stop schedules via global variables.
Write additional tests for any gaps you discover. For instance, test the new module components logic using Vitest + Vue Testing Library if feasible (this can be complex, so focus on critical logic).
Perform manual end-to-end tests on a fresh instance:
Start Directus, apply migrations, create some dummy data (partners, customers, etc.) via the UI, and verify the extensions (like documents generation, log export, etc.) function in a real scenario.
Test the login flow with Keycloak if possible (or simulate by hitting the callback URL with a fabricated code and token).
Try out edge cases: invalid inputs (like missing fields, or unauthorized access). Ensure the API returns appropriate errors (400 for bad request as done in many places, 403 for forbidden, etc.) and the UI handles them (e.g., shows a notification).
Step 8: Iterate (Closed-Loop Corrections)
Throughout steps 2–7, adopt an iterative approach:
After implementing each module’s changes, run its tests immediately. For example, once you refactor nucleus-support, write/run tests for ticket creation and retrieval. Fix bugs (maybe you realize you forgot to add a status field in schema, or the ItemsService needs correct accountability).
Integrate changes incrementally into the running app to catch integration issues early. If the support endpoints work via API, check the Directus UI for tickets (the item may not show if permissions are wrong – adjust then).
If any feature is not meeting the acceptance criteria from the README, rework it until it does. For instance, if the Keycloak login still feels hacky, refine it or consult Directus forums for proper SSO integration approach.
Use logging (to server logs) liberally while debugging, then clean up logs in final code or switch to debug level.
Continue this loop: implement → test → fix until all features are robust.
Step 9: Final Cleanup and Documentation
Remove any debug code, ensure all console logs are either removed or downgraded to debug logs.
Double-check that no sensitive info is logged (tokens, passwords).
Update all READMEs in extensions/* to describe the new usage accurately (this serves as documentation for future maintainers and to verify nothing is placeholder).
In docs/ (e.g., setup.md or a new README section), write instructions on how to enable and use these extensions (for instance: how to configure Keycloak env vars, how to schedule the Tenable sync, etc.).
Bump version numbers of extensions to signal they are now complete.
Commit all changes and run CI one more time to ensure everything passes.
By following the above steps methodically for each component, you will eliminate placeholder logic and achieve a fully integrated solution. Perform each change in isolation, run tests, and correct course as needed (closed-loop). Only proceed to the next extension once the current one meets all criteria (functional logic, UI integration, tests passing). This approach ensures that by the end, each extension module is production-ready, seamlessly integrated into Directus, and verified by tests.
