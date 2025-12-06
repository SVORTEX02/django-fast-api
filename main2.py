from fastapi import FastAPI,Depends,status,HTTPException
from studentDTO import StudentDTO
from models import Student
from database import engine, SessionLocal
from pydantic import BaseModel
from typing import Annotated
import models
from sqlalchemy.orm import Session


app = FastAPI()

models.Student.__table__.create(bind=engine, checkfirst=True)
models.Base.metadata.create_all(bind=engine)


class PostBase(BaseModel):
    title:str
    content:str
    user_id:int
    
class UserBase(BaseModel):
    username:str
    
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]


# to create a user
@app.post("/users/",status_code=status.HTTP_201_CREATED)
async def create_user(user:UserBase,db:db_dependency):
    db_user=models.User(**user.dict())
    db.add(db_user)
    db.commit()
    
# to fetch the user

@app.get("/users/{user_id}",status_code=status.HTTP_200_OK)
async def read_user(user_id:int,db:db_dependency):
    user=db.query(models.User).filter(models.User.id==user_id).first()
    if user is None:
        raise HTTPException(status_code=404,detail="User Not Found")
    return user








@app.post('/student')
def insert(obj:StudentDTO,db: Session = Depends(get_db)):
    new_student = Student(**obj.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

@app.get('/student')
def view(db: Session = Depends(get_db)):
    return db.query(Student).all()

@app.get('/student/{student_id}') 
def get_student(student_id: int,db: Session =  Depends(get_db)):
    return db.query(Student).filter(Student.id == student_id).first()

@app.delete('/student/{student_id}') 
def delete_student(student_id: int,db: Session =  Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student:
        db.delete(student)
        db.commit()
    return student

