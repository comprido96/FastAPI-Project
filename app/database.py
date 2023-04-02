# import time
# import psycopg
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URI = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:\
    {settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# while True:
#    try:
#        conn = psycopg.connect("host=localhost port=5432 dbname=fastapi-project user=postgres password=tunztunzdiahane",
#                               cursor_factory=psycopg.ClientCursor)
#        cursor = conn.cursor()
#        print('Database connection was succesful')
#        break
#    except Exception as err:
#        print("Connecting to db failed")
#        print("Error: ", err)
#
#        time.sleep(2)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
