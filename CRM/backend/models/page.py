"""CMS page model."""

from sqlalchemy import Boolean, Column, Integer, String

from ..database import Base


class Page(Base):  # pylint: disable=too-few-public-methods
    """Generic page entry for the CMS."""

    __tablename__ = "pages"
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True)
    content = Column(String, default="")
    published = Column(Boolean, default=False)
