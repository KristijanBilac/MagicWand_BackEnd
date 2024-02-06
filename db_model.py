from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Numeric, Enum, ForeignKey

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

    magic_wands = relationship("MagicWand", back_populates="owner")


class MagicWand(Base):
    __tablename__ = 'magic_wands'

    wand_id = Column(Integer, primary_key=True, autoincrement=True)
    flexibility = Column(String(50), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.user_id"))
    length = Column(Numeric, nullable=False)
    wood = Column(Enum('alder', 'acacia', 'apple', 'ash', 'blackthorn', 'cherry'), nullable=False)

    owner = relationship("User", back_populates="magic_wands")