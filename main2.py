from fastapi import FastAPI,Depends
app = FastAPI()
from studentDTO import StudentDTO
from models import Student
from database import engine, SessionLocal

import models
models.Student.__table__.create(bind=engine, checkfirst=True)

from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

