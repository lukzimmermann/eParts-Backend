from models import User
from src.utils.database import Database

session = Database()

results = session.query(User).all()

for r in results:
    print(len(r.password_hash))