from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from app.db.base import Base

class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(String(100), nullable=True, index=True)
    content_type_id = Column(String(100), nullable=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    content_type = Column(String(100), nullable=False, index=True)
    addr1 = Column(Text, nullable=True)
    addr2 = Column(Text, nullable=True)
    zipcode = Column(String(50), nullable=True)
    tel = Column(String(100), nullable=True)
    mapx = Column(String(100), nullable=True)
    mapy = Column(String(100), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    firstimage = Column(Text, nullable=True)
    firstimage2 = Column(Text, nullable=True)
    createdtime = Column(String(50), nullable=True)
    modifiedtime = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())