import os
from contextlib import contextmanager

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

load_dotenv()
Base = declarative_base()
DATABASE_URL = (f"mysql+mysqlconnector://"
                f"{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:3306/scam_coin")
engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=5)
session_factory = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
    db = session_factory()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def transaction(db: Session):
    try:
        yield
        db.commit()
    except:
        db.rollback()
        raise
