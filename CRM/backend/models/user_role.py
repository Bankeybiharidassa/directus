"""Linking table between users and roles."""

from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint

from ..database import Base


class UserRole(Base):  # pylint: disable=too-few-public-methods
    """Assignment of a role to a user."""

    __tablename__ = "user_roles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    __table_args__ = (UniqueConstraint("user_id", "role_id", name="_user_role_uc"),)
