import os

from dotenv import load_dotenv
from schemas import Base
from sqlalchemy import create_engine

load_dotenv()

host = os.getenv('RENDER_HOST')
user = os.getenv('RENDER_USER')
pswd = os.getenv('RENDER_PASSWORD')
database = os.getenv('RENDER_DATABASE')

engine = create_engine(f'postgresql+psycopg2://{user}:{pswd}@{host}/{database}')

def create_database():
    Base.metadata.create_all(bind=engine)
    print('Tables created!')

if __name__ == '__main__':
    create_database()
