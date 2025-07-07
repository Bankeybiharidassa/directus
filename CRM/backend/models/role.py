"""User role model."""

from sqlalchemy import Column, Integer, String

from ..database import Base


class Role(Base):  # pylint: disable=too-few-public-methods
    """Role assigned to users for authorization."""

    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
