from fastapi import FastAPI, Request,Path,HTTPException,Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,JSONResponse
import json
from fastapi import status
from pydantic import BaseModel,EmailStr,AnyUrl,Field,ValidationError,computed_field
from typing import List,Dict,Optional,Annotated,Literal

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


@app.post('/hellau/{id}')
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




def load_emp():
    with open('emp.json','r') as f:
        data2=json.load(f)
    return data2

@app.get('/emp')
def view_emp():
    x=load_emp()
    return x

@app.get('/filtered_emp/{emp_id}')
def filter_emp(emp_id:int=Path(...,Title="EMPLOYEE DETAIL FETCHING",description="Provide Us the employeeId Between(1-50)",example="1,2,or 40")):
    d=load_emp()
    for emp in d:
        if emp['id']== emp_id:
            return emp 

    raise HTTPException(status_code=400, detail="PLease ENter a Valid Employee Id")



class Employee(BaseModel):
    id: int=Field(max_length=2,strict=True)
    name: Annotated[str,Field(max_length=100,title='Name of patient',description='dont Enter the digtis',examples=['Nitish','Amit'])]
    age: int =Field(ge=1,le=99)
    department:str=Field(min_length=2,strict=True)
    email:str
    # strict =True de rha h mtlb k type coercion nhi hoga mtlb "30" agr input h toh 30 nhi hopyga
    
    
    @field_validator('age',mode='before')
    def check_age(cls, value):
        if value < 18:
            raise ValueError("Employee must be at least 18")
        return value
    
emp_database=[]

@app.post("/empData_send")
def send_emp(emp: Employee):
        emp_database.append(emp.dict())
        return {"message": "Employee added", "data": emp}

    

@app.get("/emp_base")
def get_emp():
    return emp_database 

class Address(BaseModel):
    house_number: str = Field(..., example="221B")
    street_name: str = Field(..., example="Baker Street")
    area: str = Field(..., example="Andheri East")
    landmark: str = Field(None, example="Near Metro Station")
    city: str = Field(..., example="Mumbai")
    district: str = Field(None, example="Mumbai Suburban")
    state: str = Field(..., example="Maharashtra")
    country: str = Field(..., example="India")
    postal_code: str = Field(..., pattern=r"^\d{5,6}$", example="400001")

class Student(BaseModel):
    student_id: int = Field(..., gt=0, le=99, description="Age of the user")
    name: str = Field(..., max_length=50, description="Unknown Naam Likhyo apna idhr")
    address: Address
database = []


@app.post("/student_details", status_code=status.HTTP_201_CREATED)
def send_details(stud: Student):
    try:
        with open("student.json", "r") as f:
            database_data = json.load(f)
    except:
        database_data = []

   
    database_data.append(stud.model_dump())

    return database_data

class Patient(BaseModel):
    id:Annotated[str,Field(...,description="ID of the patient",examples=['P001'])]
    name:Annotated[str,Field(...,description="Name of the patient")]
    city:Annotated[str,Field(...,description="Name of city the patient livin")]
    age:Annotated[int,Field(...,gt=0,lt=120,description="Age of the patient")]
    gender:Annotated[Literal['male','female','others'],Field(...,description="Gender of Patient")]
    height:Annotated[float,Field(...,gt=0,description="Height of the patient in meters")]
    weight:Annotated[float,Field(...,gt=0,description="Weight of the patient in kg")]
    
    
    # agr existing field s koi new field banani ho toh 
    # computed field ka concept use m aata h
    @computed_field
    @property
    def bmi(self)->float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi <18.5:
            return 'Under Weight'
        elif self.bmi<25:
            return 'Normal'
        elif self.bmi<30:
            return 'Normal'
        else:
            return 'Obese'

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f, indent=4)

@app.post('/create')
def create_patient(patient:Patient):
    #pehle existing data ko load krnge
    data=load_data()

    # check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400,detail='Patient already exists')

    #if not then create new patient to the database
    data[patient.id]=patient.model_dump(exclude=['id'])
    # save into the json file
    save_data(data)
    
    return JSONResponse(status_code=201,content={"message":"Patient Created Successfully"})
    
    



class PatientUpdate(BaseModel):
    name: Annotated[
        Optional[str],
        Field(default=None, description="Name of the patient")
    ]
    city: Annotated[
        Optional[str],
        Field(default=None, description="Name of the city the patient lives in")
    ]
    age: Annotated[
        Optional[int],
        Field(default=None, gt=0, lt=120, description="Age of the patient")
    ]
    gender: Annotated[
        Optional[Literal['male', 'female', 'others']],
        Field(default=None, description="Gender of Patient")
    ]
    height: Annotated[
        Optional[float],
        Field(default=None, gt=0, description="Height in meters")
    ]
    weight: Annotated[
        Optional[float],
        Field(default=None, gt=0, description="Weight in kg")
    ]

@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data=load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404,detail="Patient Not Found")

    existing_patient_info=data[patient_id]
    print(data[patient_id])
    
    
    updated_patient_info=patient_update.model_dump(exclude_unset=True)
    
    for key,value in updated_patient_info.items():
        existing_patient_info[key]=value
    
    existing_patient_info["id"]=patient_id
    
    patient_pydantic_obj=Patient(**existing_patient_info)
    patient_pydantic_obj.model_dump(exclude=['id'])
    
    
    
    data[patient_id]=existing_patient_info
    save_data(data)
    
    return JSONResponse(status_code=200,content={'message':'Patient Updated'})


@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str):
    
    data=load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404,detail="Patient Not Found")

    del data[patient_id]
    save_data(data)
    
    return JSONResponse(status_code=200,content={"message":"Patient Deleted"})



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
    
    
def load_players():
    with open('players.json','r') as f:
        data = json.load(f)
        return data

def save_player(data):
    with open('players.json', 'w') as f:
        json.dump(data, f, indent=4)

@app.post('/new_player')
def add_players(new_player:Player):
    data=load_players()
    
    if any(player["id"] == new_player.id for player in data):
        raise HTTPException(status_code=404, detail="Player duplicacy, enter unique details")

    
    new_info=new_player.model_dump()
    
    data.append(new_info) 
    save_player(data)
    
    return JSONResponse(status_code=200,content={"message":"Thank U have a new player added "})



class UPDStats(BaseModel):
    appearances: Optional[int] = None
    goals: Optional[int] = None
    assists: Optional[int] = None

class UPDPlayer(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    age: Optional[int] = None
    position: Optional[str] = None
    club: Optional[str] = None
    nationality: Optional[str] = None
    jersey_number: Optional[int] = None
    stats: Optional[UPDStats] = None
    

@app.put('/edit_players/{player_id}')
def edit_player(player_id: int, upd_player: UPDPlayer):
    data = load_players()
    
    for player in data:
        if player["id"] == player_id:
            update_info = upd_player.model_dump(exclude_unset=True)

            # Handle nested stats separately
            if "stats" in update_info:
                stats_update = update_info["stats"].model_dump(exclude_unset=True)
                existing_stats = player.get("stats", {})
                existing_stats.update(stats_update)
                player["stats"] = existing_stats
                del update_info["stats"]

            
            player.update(update_info)

            save_player(data)
            return {"message": "Player updated successfully"}
    
    
    raise HTTPException(status_code=404, detail="Player not found")
