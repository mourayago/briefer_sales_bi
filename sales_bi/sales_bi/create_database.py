import os

from dotenv import load_dotenv
from schemas import Base
from sqlalchemy import create_engine

load_dotenv()

database_url = os.getenv('URI')

engine = create_engine(database_url)

Base.metadata.create_all(bind=engine)

print('Tables created!')
