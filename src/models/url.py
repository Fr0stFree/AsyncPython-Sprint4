from uuid import uuid4

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from db import Base


class Url(Base):
    __tablename__ = 'url'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    full_url = Column(String(255), nullable=False, unique=True, index=True)
    clicks = Column(Integer, nullable=False, default=0)
