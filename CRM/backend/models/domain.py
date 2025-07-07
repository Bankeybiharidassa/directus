"""Tenant domain configuration."""

from sqlalchemy import Column, ForeignKey, Integer, String

from ..database import Base


class Domain(Base):  # pylint: disable=too-few-public-methods
    """Domain settings for customer mail."""

    __tablename__ = "domains"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    domain = Column(String, index=True)
    imap_host = Column(String, nullable=True)
    imap_user = Column(String, nullable=True)
    imap_password = Column(String, nullable=True)
    smtp_host = Column(String, nullable=True)
    smtp_user = Column(String, nullable=True)
    smtp_password = Column(String, nullable=True)
