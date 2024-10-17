from sqlalchemy import Column, Date, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Sales table Schema
class Sales(Base):
    __tablename__ = 'sales'

    registrer_id = Column(Integer, primary_key=True, autoincrement=True)
    seller_id = Column(Integer, nullable=False)
    seller_name = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    sales_date = Column(Date, nullable=False, index=True)
    sales_value = Column(Float, nullable=False)


# Target table Schema
class Targets(Base):
    __tablename__ = 'targets'

    registrer_id = Column(Integer, primary_key=True, autoincrement=True)
    seller_id = Column(Integer, nullable=False)
    date_ref = Column(Date, nullable=False)
    target_value = Column(Float, nullable=False)
