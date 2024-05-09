
from typing import List
from sqlalchemy import ARRAY, Boolean, Column, Float, ForeignKey, String, Integer, Sequence,  DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base




Base = declarative_base()


class Expenditure(Base):
    __tablename__ = "expenditures"

    
    id_user = Column(Integer, index=True)
    amount =  Column(Float)
    id_group = Column(Integer, index=True)
    description = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    id_expenditure = Column(Integer, Sequence('expenditure_id_seq'), primary_key=True)

class User(Base):
    __tablename__ = "users"

    
    id_user = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    username = Column(String)
    password = Column(String)
    token = Column(String)
    mail = Column(String)
    celular = Column(String)

class Group(Base):
    __tablename__ = "groups"
    
    id_group = Column(Integer,primary_key=True)
    name = Column(String)
    members_count = Column(Integer)
    time_created = Column(DateTime(timezone=True), server_default=func.now())

class GroupMembers(Base):
    __tablename__ = "groupMembers"
      
    id_group = Column(Integer, ForeignKey('groups.id_group', ondelete='CASCADE'), primary_key=True)
    id_user = Column(Integer, ForeignKey('users.id_user', ondelete='CASCADE'), primary_key=True)
    admin = Column(Boolean)
class GroupCategories(Base):
    __tablename__ = "groupCategories"
      
    id_group = Column(Integer, ForeignKey('groups.id_group', ondelete='CASCADE'), primary_key=True)
    id_category = Column(Integer, ForeignKey('categories.id_category', ondelete='CASCADE'), primary_key=True)
class Category(Base):
    __tablename__ = "categories"
     
    id_category = Column(Integer,  Sequence('categoryid_seq'), primary_key=True)
    name = Column(String)