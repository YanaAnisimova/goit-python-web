from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
_CONNECTION = 'postgresql://postgres:123456@localhost/module_09'

engine = create_engine(_CONNECTION, echo=False)
metadata = Base.metadata
DBSession = sessionmaker(bind=engine)
session = DBSession()