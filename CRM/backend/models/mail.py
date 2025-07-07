"""Database model for archived mail messages."""

from sqlalchemy import Column, DateTime, Integer, String

from ..database import Base


class MailMessage(Base):  # pylint: disable=too-few-public-methods
    """Mail message metadata."""

    __tablename__ = "mail_messages"
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(String, unique=True, index=True)
    sender = Column(String)
    subject = Column(String)
    date = Column(DateTime)
