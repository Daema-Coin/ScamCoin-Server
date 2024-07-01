import os
from contextlib import contextmanager

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

load_dotenv()
Base = declarative_base()
DATABASE_URL = (f"mysql+mysqlconnector://"
                f"{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:3306/scam_coin")
engine = create_engine(DATABASE_URL)
session_factory = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Session = scoped_session(session_factory=session_factory)


def get_db():
    db = Session()
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
