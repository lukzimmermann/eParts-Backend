import os
from src.utils import singleton
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

@singleton
class Database():
    def __init__(self) -> None:
        engine = create_engine(os.getenv('DATABASE_URL'), echo=True)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        return self.session
