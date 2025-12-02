from pydantic import BaseModel,EmailStr,AnyUrl,Field
from typing import List,Dict,Optional,Annotated
class Patient(BaseModel):
    # name:str=Field(max_length=100)
    name:Annotated[str,Field(max_length=100,title='Name of patient',description='dont Enter the digtis',examples=['Nitish','Amit'])]
    age:int 
    email:EmailStr
    linkedIn_Url:AnyUrl
    weight:float=Field(gt=0)
    married:bool=False
    allergy:Optional[List[str]]=None 
    contact_details:Dict[str,str]


def inert_patient(patient:Patient):
    print(f"{patient.name}{patient.age}{patient.allergy}{patient.contact_details}")

patient_info={'name':'nitish kumar reddy','age':30,'weight':76.66,'married':True,'allergy':['pollan','dust'],'contact_details':{'email':'shrey02@gmail.com','phone':'459634950'}}
patient=Patient(**patient_info)


inert_patient(patient)