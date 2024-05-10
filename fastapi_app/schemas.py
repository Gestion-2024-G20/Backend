
from sqlalchemy import Boolean, Column, Float, ForeignKey, String, Integer, Sequence,  DateTime
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
class GroupMember(Base):
    __tablename__ = "groupMembers"
      
    id_group = Column(Integer, ForeignKey('groups.id_group', ondelete='CASCADE'), primary_key=True)
    id_user = Column(Integer, ForeignKey('users.id_user', ondelete='CASCADE'), primary_key=True)
    is_admin = Column(Boolean)
      
class CategoryShare(Base):
    __tablename__ = "categoryShares"
     
    id_group = Column(Integer, ForeignKey('groups.id_group', ondelete='CASCADE'), primary_key=True)
    id_user = Column(Integer,  ForeignKey('users.id_user', ondelete='CASCADE'), Sequence('id_user'), primary_key=True)
    category_name = Column(String, primary_key=True)
    share_percentage = Column(Integer)