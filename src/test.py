from models import User
from utils.database import Database
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

session = Database().get_session()

# user = User()
# user.name = "Nati"
# user.password_hash = pwd_context.hash("nati")

# session.add(user)
# session.commit()

results = session.query(User).all()

for r in results:
    print(r)