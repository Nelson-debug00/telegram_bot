from database import Base
from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime

class PrecioDolar(Base):
    __tablename__ = "precios_dolar"
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.now, nullable=False)

class PrecioEuro(Base):
    __tablename__ = "precios_euro"
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.now, nullable=False)

class PrecioUsdt(Base):
    __tablename__ = "precios_usdt"
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.now, nullable=False)
