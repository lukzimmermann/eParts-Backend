import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from utils.singleton import singleton
from sqlalchemy.orm import sessionmaker

load_dotenv()

@singleton
class Database():
    def __init__(self) -> None:
        engine = create_engine(os.getenv('DATABASE_URL'), echo=False)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_session(self):
        return self.session
