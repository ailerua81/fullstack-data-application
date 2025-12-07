from pydantic import BaseModel, ConfigDict
from typing import Optional


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    password: str
    firstName : Optional[str] = None
    lastName : Optional[str] = None
    email : Optional[str] = None
    role : str = "benevole"  # admin, fondateur, benevole

class UserOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    username: str
    firstName : Optional[str] = None
    lastName : Optional[str] = None
    email : Optional[str] = None
    role : str
    
    model_config = {"from_attributes": True}
