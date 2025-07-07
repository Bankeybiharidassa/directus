from sqlalchemy import Column, Integer, String

from ..database import Base


class WhitelistedIP(Base):  # pylint: disable=too-few-public-methods
    """Whitelist entry for IP, CIDR or FQDN patterns."""

    __tablename__ = "whitelisted_ips"
    id = Column(Integer, primary_key=True, index=True)
    pattern = Column(String, unique=True, index=True)
