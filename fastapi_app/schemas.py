from pydantic import BaseModel
from datetime import datetime
from typing import Optional



class ExpenditureBase(BaseModel):
	id_user: int
	amount: float
	id_group: int
	description : str

class Expenditure(ExpenditureBase):
	time_created: str

    
class UserBase(BaseModel):
	id_user : int
	password : str
	token : str
	mail : str
	celular : str

class GroupBase(BaseModel):
	name : str
 
class Group(GroupBase):
	id_group : int
	time_created: str