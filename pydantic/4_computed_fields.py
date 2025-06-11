from pydantic import BaseModel, EmailStr, computed_field
from typing import List, Dict, Annotated

class Patient(BaseModel): # Pydantic model
    name: str 
    age: int 
    email: EmailStr
    weight: float # kg
    height: float # meter
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str] # key, value type


    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height ** 2), 2)
        return bmi


def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.bmi)
    print("Inserted into database")


patient_info = {
    "name": "mahadi",
    "age": 70,
    "email": "abc@icici.com",  # Invalid domain
    "weight": 75.5,
    "height": 1.72,
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