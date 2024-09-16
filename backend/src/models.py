from sqlalchemy import Boolean, Column, DateTime, String, Integer, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    password_hash = Column(String(128))
    create_at = Column(DateTime, default=func.now())
    update_at = Column(DateTime)
    disabled = Column(Boolean, default=False)

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}"