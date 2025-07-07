"""Store third-party API configuration settings."""

from sqlalchemy import Column, Integer, String

from ..database import Base


class ApiConfig(Base):  # pylint: disable=too-few-public-methods
    """External API credentials."""

    __tablename__ = "api_config"
    id = Column(Integer, primary_key=True, index=True)
    api_key = Column(String, nullable=False)
    model = Column(String, nullable=False)
