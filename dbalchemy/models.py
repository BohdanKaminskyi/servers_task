from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
    password_hash = Column(String)
    salt = Column(String)

    def __repr__(self):
        return f"<User(first_name={self.first_name}, last_name={self.last_name})>"
