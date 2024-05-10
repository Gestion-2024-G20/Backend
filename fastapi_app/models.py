from pydantic import BaseModel
from typing import List

from pyparsing import Any



class ExpenditureBase(BaseModel):
	id_user: int
	amount: float
	id_group: int
	description : str

class Expenditure(ExpenditureBase):
	time_created: str

    
class User(BaseModel):
	id_user : int
	username: str
	password : str
	token : str
	mail : str
	celular : str

class Group(BaseModel):
	id_group : int
	name: str
	members_count: int
	time_created: str
class GroupMember(BaseModel):
	id_group : int
	id_user : int
	is_admin : bool
class CategoryShare(BaseModel):
    id_group : int 
    id_user : int
    category_name : str
    name : str

class ResponseModel(BaseModel):
    code:int
    message:str
    detail:str
    dataModel:Any