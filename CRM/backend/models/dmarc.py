"""DMARC reporting models."""

from sqlalchemy import Column, Float, Integer, String

from ..database import Base


class DmarcReport(Base):  # pylint: disable=too-few-public-methods
    """Aggregated DMARC statistics."""

    __tablename__ = "dmarc_reports"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, index=True)
    domain = Column(String, index=True)
    pass_count = Column(Integer, default=0)
    fail_count = Column(Integer, default=0)
    volume = Column(Integer, default=0)
    abuse_contacts = Column(Integer, default=0)
    complaint_rate = Column(Float, default=0.0)


class DmarcAbuse(Base):  # pylint: disable=too-few-public-methods
    """Abuse reports sent to domain contacts."""

    __tablename__ = "dmarc_abuse"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, index=True)
    domain = Column(String, index=True)
    ip_address = Column(String, index=True)
    contact = Column(String)
    status = Column(String, default="sent")
