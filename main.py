from fastapi import FastAPI, Request,Path,HTTPException,Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import json
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



@app.get('/patient/{patient_id}')
def view_patient(patient_id:str=Path(...,description='ID of the patient in the DB',example='P001')):
    # load all the patients
    data =load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail='Patient Not Found')

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
# dgjnrg