"""Database model for end customers."""

from sqlalchemy import Column, Integer, String

from ..database import Base


class Customer(Base):  # pylint: disable=too-few-public-methods
    """CRM customer record."""

    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    contact_email = Column(String, index=True)
    # partner or customer to determine Sophos API workflow
    sophos_api_mode = Column(String, default="customer", server_default="customer")
