"""Support ticket model."""

from sqlalchemy import Column, ForeignKey, Integer, String

from ..database import Base


class Ticket(Base):  # pylint: disable=too-few-public-methods
    """Ticket for the support desk."""

    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(String, default="open")
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
