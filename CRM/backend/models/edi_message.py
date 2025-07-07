"""Persistent storage for EDI messages."""

from sqlalchemy import Column, Integer, String

from ..database import Base


class EdiMessage(Base):  # pylint: disable=too-few-public-methods
    """EDI message record."""

    __tablename__ = "edi_messages"
    id = Column(Integer, primary_key=True, index=True)
    sender_type = Column(String, nullable=False)
    sender_id = Column(Integer, nullable=False)
    receiver_type = Column(String, nullable=False)
    receiver_id = Column(Integer, nullable=False)
    content = Column(String, nullable=False)
