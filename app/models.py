from sqlalchemy import Column, Integer, String , Index
from .database import Base
from sqlalchemy import DateTime
from datetime import datetime

created_at = Column(DateTime)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone_number = Column(String)
    created_at = Column(DateTime)

    __table_args__ = (
        Index("ix_users_email", "email"),
    )