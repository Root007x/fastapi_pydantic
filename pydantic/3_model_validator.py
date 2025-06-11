from pydantic import BaseModel, EmailStr, model_validator
from typing import List, Dict, Annotated

class Patient(BaseModel): # Pydantic model
    name: str 
    age: int 
    email: EmailStr
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str] # key, value type

    @model_validator(mode = "after")
    def validate_emergency_contact(cls, model):
        if model.age > 60 and "emergency" not in model.contact_details:
            raise ValueError("Patients older than 60 must have an emergency contact")
        return model

def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("Inserted into database")


patient_info = {
    "name": "mahadi",
    "age": 70,
    "email": "abc@icici.com",  # Invalid domain
    "weight": 55.5,
    "married": True,
    "allergies": ["pollen", "dust"],
    "contact_details": {
        "email": "abc@gmail.com",
        "phone": "324234234",
        "emergency": "22222"
    }
}


patient_1 = Patient(**patient_info) 


insert_patient_data(patient_1)