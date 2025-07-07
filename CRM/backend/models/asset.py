"""Database model for tracked assets."""

from sqlalchemy import Column, Integer, String

from ..database import Base


class Asset(Base):  # pylint: disable=too-few-public-methods
    """Asset entry for inventory management."""

    __tablename__ = "assets"
    id = Column(Integer, primary_key=True, index=True)
    hostname = Column(String, unique=True, index=True)
    status = Column(String, default="unknown")
