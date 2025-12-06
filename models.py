from sqlalchemy import Column, Integer, String,Boolean
from database import Base

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    age = Column(Integer)
    
    
class User(Base):
    __tablename__="users"
    
    id = Column(Integer,primary_key=True,index=True)
    username=Column(String(50),unique=True)
    
class Post(Base):
    __tablename__="posts"
    
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String(50))
    content=Column(String(100))
    user_id=Column(Integer)
    