from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Annotated

class Patient(BaseModel): # Pydantic model
    name: str = Field(max_length=50)
    age: int = Field(gt=0, lt=120)
    email: EmailStr
    linked_in: AnyUrl
    weight: Annotated[float, Field(gt=0, strict=True)]
    married: Annotated[bool, Field(default=None, description="Is the patient married or not")]
    allergies: List[str] = Field(max_length=5)
    contact_details: Dict[str, str] # key, value type

def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("Inserted into database")


patient_info = {"name": "mahadi", "age": 30,"email": "abc@gmail.com","linked_in": "https://www.linkedin.com/feed/", "weight": 55.5, "married": True, "allergies": ["pollen", "dust"], "contact_details": {"email": "abc@gmail.com","phone": "324234234"}}


patient_1 = Patient(**patient_info) 


insert_patient_data(patient_1)