"""Configuration options for Keycloak integration."""

from sqlalchemy import Column, Integer, String

from ..database import Base


class KeycloakConfig(Base):  # pylint: disable=too-few-public-methods
    """Keycloak server details."""

    __tablename__ = "keycloak_config"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    realm = Column(String, nullable=False)
    client_id = Column(String, nullable=False)
    client_secret = Column(String, nullable=False)
