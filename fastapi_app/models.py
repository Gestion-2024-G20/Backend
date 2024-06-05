from typing import List, Optional

from pydantic import BaseModel
from pyparsing import Any

class ExpenditureBase(BaseModel):
	id_user: int
	amount: float
	id_group: int
	description : str
	id_expenditure : int
	id_category: int

class ExpenditureComplete(ExpenditureBase):
	time_created: str
	name_category: str

class User(BaseModel):
	id_user : int
	username: str
	password : str
	name: str
	lastname: str
	token : str
	mail : str
	celular : str
	profile_image_name : str

class GroupBase(BaseModel):
	id_group : int
	name: str
	members_count: int
	description: Optional[str]

class Group(GroupBase):
	time_created: str
	is_deleted: bool
 
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

#Clase invitación
class Invitation(BaseModel):
	id_invitation : int
	id_group : int
	id_user : int
	is_request : bool


class BalanceItem(BaseModel):
	id_user: int
	username: str
	amount: float

class Balance(BaseModel):
	to_pay: List[BalanceItem]
	to_receive: List[BalanceItem]

class Request(BaseModel):
	id_request : int
	id_group : int
	token : str
	time_created : str