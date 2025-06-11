from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Dict, Annotated

class Patient(BaseModel): # Pydantic model
    name: str 
    age: int 
    email: EmailStr
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str] # key, value type

    @field_validator("email")
    @classmethod
    def email_validator(cls, value):
        valid_domain = ["icici.com", "hdfc.com"]
        domain_name = value.split('@')[-1]

        if domain_name not in valid_domain:
            raise ValueError("Not a valid domain")
        return value

def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("Inserted into database")


patient_info = {
    "name": "mahadi",
    "age": 30,
    "email": "abc@icici.com",  # Invalid domain
    "weight": 55.5,
    "married": True,
    "allergies": ["pollen", "dust"],
    "contact_details": {
        "email": "abc@gmail.com",
        "phone": "324234234"
    }
}


patient_1 = Patient(**patient_info) 


insert_patient_data(patient_1)