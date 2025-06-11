from pydantic import BaseModel

class Address(BaseModel):
    city: str
    state: str
    pin : str


class Paitent(BaseModel):

    name : str
    gender : str
    age : int
    address : Address


address_dict = {"city": "Dhaka", "state": "Shajadpur", "pin": "1212"}

address_1 = Address(**address_dict)

patient_dict = {
    "name" : "Hasan",
    "gender": "male",
    "age" : 25,
    "address" : address_1
}

# It converts the Pydantic model instance back into a dictionary.
patient_1 = Paitent(**patient_dict)

temp = patient_1.model_dump()

print(temp)
print(type(temp))