from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///biblioteca.db') 
Session = sessionmaker(bind=engine) 
sessionobj = Session()
Base = declarative_base() 