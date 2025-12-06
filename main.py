from fastapi import FastAPI, Request,Path,HTTPException,Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import json

from pydantic import BaseModel,EmailStr,AnyUrl,Field,ValidationError
from typing import List,Dict,Optional,Annotated

from pydantic import field_validator

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# @app.get("hello/")
# def hell():
#     return {'message':'Hllo World in FastApi'}

# @app.get("/", response_class=HTMLResponse)
# def home(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})


# @app.get("/api/message")
# def message_api():
#     return {"message": "This is a simple API!"}



# # API (STATIC DATA)
# @app.get("/api/user")
# def get_user():
#     return {
#         "name": "Shrey",
#         "age": 22,
#         "city": "Delhi"
#     }
def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)
    return data

@app.get("/")
def hello():
    return {'message':'Patient Managemet System'}

@app.get('/about')
def about():
    return {'message':'About '}

@app.get('/view')
def view():
    data=load_data()
    return data


@app.get('/hella/{id}')
def view_ply(id:int=Path(...,description="jersey number of the player",example=7)):
    with open('players.json','r') as f:
        data = json.load(f)
    
    player = next((p for p in data if p['id'] == id), None)
    if player:
        return player
    
    raise HTTPException(status_code=404, detail='Player not Found')


@app.post('/hella/{id}')
def view_ply(id:int=Path(...,description="jersey number of the player",example=7)):
    with open('players.json','r') as f:
        data = json.load(f)
    
    player = next((p for p in data if p['id'] == id), None)
    if player:
        return player
    
    raise HTTPException(status_code=404, detail='Player not Found')



@app.get('/patient/{patient_id:P\\d{3}}')
def view_patient(patient_id: str = Path(..., description='ID of the patient in the DB',regex="^P\\d{3}$" , example='P001')):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient Not Found')




@app.get('/sort')
def sort_patients(
    sort_by: str = Query(..., description="Sort using height, weight, or bmi"),
    order: str = Query("asc", description="Order: asc or desc")
):
    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field. Select from {valid_fields}")

    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Order must be 'asc' or 'desc'")

    data = load_data()

    reverse_flag = True if order == "desc" else False

    sorted_data = sorted(
        data.values(),
        key=lambda x: x.get(sort_by, 0),
        reverse=reverse_flag
    )

    return sorted_data



class Stats(BaseModel):
    appearances: int
    goals: int | None = None
    assists: int | None = None

class Player(BaseModel):
    id: int
    name: str
    age: int
    position: str
    club: str
    nationality: str
    jersey_number: int
    stats: Stats
    
    
    @field_validator("age")
    def check_age(cls, v):
        if v <= 0:
            raise ValueError("Age must be positive")
        return v
    
    
with open('players.json','r') as f:
    data = json.load(f)

with open('players.json','r') as f:
    data = json.load(f)

players = [Player(**player) for player in data]

print(players)


class Title(BaseModel):
    title:str
    year:int
    rating:float
    
    @field_validator("year")
    def check(cls,v):
        if v<=0:
            raise ValueError("Year must be in positive")
        return v
    
    
    
class User(BaseModel):
    username:Annotated[str,Field(min_length=2,max_length=100)]
    email:str
    age:Annotated[int,Field(ge=12,le=100)]
    
    @field_validator("age")
    def check(cls,v):
        if v<=0:
            raise ValueError("Year must be in positive")
        return v
    
try:  
    user1=User(username="Vortex",email="vortex@gmail.com",age="30")
except ValidationError as e:
    print(e)
    

# print(user1)

# print(user1.model_dump())

# print(user1.model_dump_json(indent=4))