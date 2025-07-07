"""Database model for partner organizations."""

from sqlalchemy import Column, ForeignKey, Integer, String

from ..database import Base


class Partner(Base):  # pylint: disable=too-few-public-methods
    """Partner entity in the CRM hierarchy."""

    __tablename__ = "partners"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    parent_id = Column(Integer, ForeignKey("partners.id"), nullable=True)
    distributor_id = Column(Integer, ForeignKey("distributors.id"), nullable=True)
