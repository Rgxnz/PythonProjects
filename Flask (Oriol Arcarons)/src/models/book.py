from src.config.db import Base
from sqlalchemy import Column, Integer, String, Numeric 

class Book(Base):
    __tablename__ = 'books' 
    id = Column(Integer, primary_key=True, autoincrement=True) 
    title = Column(String)
    author = Column(String)
    price = Column(Numeric)