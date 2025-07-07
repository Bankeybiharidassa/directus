"""Nucleus CRM FastAPI application entrypoint."""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .logging_setup import setup_logging
from .settings import apply_env

apply_env()  # pylint: disable=wrong-import-position
setup_logging()  # pylint: disable=wrong-import-position
from . import models  # pylint: disable=unused-import
from .database import Base, engine
from .routes import (
    assets,
    auth,
    cases,
    certificates,
    cms,
    config,
    contracts,
    core,
    crm,
    crm_dmarc,
    crm_domains,
)
from .routes import crm_sync as crm_sync_route
from .routes import (
    distributors,
    dmarc,
    docs,
    edi,
    ip_whitelist,
    keycloak,
    mail,
    partners,
    roles,
    sophos,
    support,
    tenable,
    tickets,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Nucleus CRM")

origins_env = os.getenv("CORS_ORIGINS", "*")
origins = (
    [o.strip() for o in origins_env.split(",") if o.strip()] if origins_env else ["*"]
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["core"], summary="API root")
def api_root():
    """Provide basic information for the API root."""
    return {"message": "Nucleus CRM backend", "docs": "/docs"}


app.include_router(auth.router)
app.include_router(crm.router)
app.include_router(cases.router)
app.include_router(docs.router)
app.include_router(mail.router)
app.include_router(assets.router)
app.include_router(tickets.router)
app.include_router(partners.router)
app.include_router(distributors.router)
app.include_router(keycloak.router)
app.include_router(cms.router)
app.include_router(contracts.router)
app.include_router(roles.router)
app.include_router(ip_whitelist.router)
app.include_router(core.router)
app.include_router(config.router)
app.include_router(certificates.router)
app.include_router(sophos.router)
app.include_router(tenable.router)
app.include_router(dmarc.router)
app.include_router(crm_dmarc.router)
app.include_router(crm_domains.router)
app.include_router(support.router)
app.include_router(crm_sync_route.router)
app.include_router(edi.router)


@app.get("/health", tags=["core"])
def health_check():
    """Return a simple health status."""
    return {"status": "ok"}
