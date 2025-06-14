from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional

# Data Validation
class Patient(BaseModel):

    id: Annotated[str, Field(..., description="Id of the patient", examples=["P001"])]
    name: Annotated[str, Field(..., description="Name of the patient")]
    city: Annotated[str, Field(..., description="City where the patient is living")]
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the patient")]
    gender: Annotated[Literal["male","female","other"], Field(..., description="Gender of the patient")]
    height: Annotated[float, Field(..., gt=0, description="Height of the patient in meter")]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the patient in kgs")]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2), 2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:

        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"
        

class PatientUpdate(BaseModel):

    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0, lt=120)]
    gender: Annotated[Optional[Literal["male","female","other"]], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt = 0)]


# main
app = FastAPI()

def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
    return data # return as dict format


def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f)


@app.get("/")
def hello():
    return {"message": "Patient Management System API"}

@app.get("/about")
def about():
    return {"message": "A fully functional API to manage your patients record"}


@app.get("/view")
def view():
    data = load_data()
    return data


@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description="ID of the Patient in the DB", example="P001")):
    data = load_data()

    if patient_id in data.keys():
        return data[patient_id]
    raise HTTPException(status_code = 404, detail = "Paitent Not Found")


@app.get("/sort")
def sort_patient(sort_by: str = Query(..., description="Sort on the basis of height, weight or bmi"), order: str = Query('asc', description="Sort in ascending or descending order")):
    
    valid_fields = ["height", "weight", "bmi"]

    if sort_by not in valid_fields:
        raise HTTPException(status_code = 400, detail = "Invalid field")

    if order not in ["asc","desc"]:
        raise HTTPException(status_code = 400, detail = "Invalid Order select between asc or desc")
    
    data = load_data()

    sort_order = True if order == "desc" else False

    sorted_data = sorted(data.values(), key = lambda x : x.get(sort_by,0), reverse = sort_order)
    
    return sorted_data


@app.post("/create")
def create_patient(patient: Patient):

    # laod data
    data = load_data()

    # check if the patient already exists
    if patient.id in data.keys():
        raise HTTPException(status_code=400, detail="Patient Aleary Exists")

    # add to the database 
    data[patient.id] = patient.model_dump(exclude=["id"]) # convert dict

    # save into the json file
    save_data(data)

    return JSONResponse(status_code=201, content={"message": "Patient created successfully"})



@app.put("/edit/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate):
    
    # laod data
    data = load_data()

    # check if the patient already exisit
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="patient not found")
    
    # load existing patient info
    existing_data = data[patient_id]


    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_data[key] = value

    # calculate bmi and verdict
    existing_data["id"] = patient_id
    patient_pydantic_obj = Patient(**existing_data)
    existing_data = patient_pydantic_obj.model_dump(exclude="id")
    
    # add dict to data
    data[patient_id] = existing_data

    save_data(data)

    return JSONResponse(status_code=200, content={"message": "Patient Updated"})



@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):

    # load data
    data = load_data()

    # check if the patient already exisit
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="patient not found")
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={"message": "Patient Deleted"})