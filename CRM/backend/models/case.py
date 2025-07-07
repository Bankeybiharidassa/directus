"""Database model for support cases."""

from sqlalchemy import Column, Integer, String

from ..database import Base


class Case(Base):  # pylint: disable=too-few-public-methods
    """Simple support case entry."""

    __tablename__ = "cases"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    namespace = Column(String, index=True)
