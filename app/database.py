from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL ="postgresql://postgres:95126688@localhost/postgres"


engine = create_engine(
  SQLALCHEMY_DATABASE_URL,
  connect_args={'client_encoding': 'UTF8'}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
