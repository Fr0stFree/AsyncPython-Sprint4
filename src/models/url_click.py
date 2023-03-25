import datetime as dt

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from db import Base


class UrlClick(Base):
    __tablename__ = 'url_clicks'
    
    url_id = Column(ForeignKey('url.id', ondelete='CASCADE'), primary_key=True)
    url = relationship('Url', back_populates='clicks')
    client = Column(String(100), primary_key=True)
    datetime = Column(DateTime, default=dt.datetime.utcnow, primary_key=True)
