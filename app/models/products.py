from app.backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    slug = Column(String, unique=True)
    description = Column(String)
    price = Column(Integer)
    image_url = Column(String)
    stock = Column(Float)
    rating = Column(Float)
    is_active = Column(Boolean, default=True)
