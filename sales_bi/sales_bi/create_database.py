from schemas import Base
from sqlalchemy import create_engine

URI = """postgresql+psycopg2://postgres:admin@localhost:5432/postgres"""

engine = create_engine(URI)

Base.metadata.create_all(bind=engine)

print('Tables created!')
