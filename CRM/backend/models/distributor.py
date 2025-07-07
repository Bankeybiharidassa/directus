"""Distributor level in CRM hierarchy."""

from sqlalchemy import Column, Integer, String

from ..database import Base


class Distributor(Base):  # pylint: disable=too-few-public-methods
    """Top-level distributor organization."""

    __tablename__ = "distributors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
