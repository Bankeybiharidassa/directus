"""Database model representing service contracts."""

from sqlalchemy import Column, Date, ForeignKey, Integer, String

from ..database import Base


class Contract(Base):  # pylint: disable=too-few-public-methods
    """Simple contract between the company and a customer."""

    __tablename__ = "contracts"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    description = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(String, default="active")
