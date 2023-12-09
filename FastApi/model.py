from fastapi import FastAPI
from database import Base
from sqlalchemy import Column,Integer,Float,Boolean,String

class Transactions(Base):
    __tablename__ = "transactions"
    id = Column(Integer,primary_key=True,index=True)
    amount = Column(Float)
    category = Column(String)
    description  = Column(String)
    is_income = Column(Boolean)
    date = Column(String)