
# create a engine to create the database

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL= 'sqlite:///./todos.db'# todos.db name akta database create hobe

engine= create_engine(SQLALCHEMY_DATABASE_URL,connect_args={'check_same_thread':False})

sessionlocal= sessionmaker(autoflush=False,autocommit=False,bind=engine)
Base = declarative_base()