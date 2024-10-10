from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


# Sales table Schema
class Sales(Base):
    __tablename__ = 'sales'

    seller_id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    state = Column(String(2), nullable=False)
    sales_date = Column(Date, nullable=False, index=True)
    value = Column(Float, nullable=False)


# Target table Schema
class Targets(Base):
    __tablename__ = 'targets'

    seller_id = Column(Integer, ForeignKey('sales.seller_id'), primary_key=True)
    date_ref = Column(Date, nullable=False)
    target = Column(Float, nullable=False)

    seller_relationship = relationship('Sales')



