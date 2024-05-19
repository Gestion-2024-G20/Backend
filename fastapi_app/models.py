from typing import List

from pydantic import BaseModel
from pyparsing import Any

class ExpenditureBase(BaseModel):
	id_user: int
	amount: float
	id_group: int
	description : str
	id_expenditure : int

class Expenditure(ExpenditureBase):
	time_created: str

class User(BaseModel):
	id_user : int
	username: str
	password : str
	token : str
	mail : str
	celular : str

class GroupBase(BaseModel):
	id_group : int
	name: str
	members_count: int

class Group(GroupBase):
	time_created: str
 
class GroupMember(BaseModel):
	id_gm : int
	id_group : int
	id_user : int
	is_admin : bool
 
class CategoryBase(BaseModel):
	id_category : int
	id_group : int
	name : str
	description : str

class CategoryShare(BaseModel):
    id_cs : int 
    id_category : int 
    id_user : int
    share_percentage : int
class ExpenditureShare(BaseModel):
    id_es : int 
    id_expenditure : int 
    id_user : int
    share_percentage : int
class ResponseModel(BaseModel):
    code:int
    message:str
    detail:str
    dataModel:Any