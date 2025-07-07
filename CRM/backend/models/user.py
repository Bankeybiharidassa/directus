"""User account model."""

from sqlalchemy import Boolean, Column, Integer, String

from ..database import Base


class User(Base):  # pylint: disable=too-few-public-methods
    """Application user."""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    portal_access = Column(Boolean, default=True)
    mfa_enabled = Column(Boolean, default=False)
    mfa_secret = Column(String, nullable=True)
    remote_access_enabled = Column(Boolean, default=False)
