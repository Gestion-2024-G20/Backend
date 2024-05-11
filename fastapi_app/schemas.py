
from sqlalchemy import Boolean, Column, Float, ForeignKey, ForeignKeyConstraint, String, Integer, Sequence,  DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Expenditure(Base):
    __tablename__ = "expenditures"

    
    id_user = Column(Integer, ForeignKey('users.id_user'))
    amount =  Column(Float)
    id_group = Column(Integer, ForeignKey('groups.id_group'))
    description = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    id_expenditure = Column(Integer, Sequence('expenditure_id_seq'), primary_key=True, index=True)
class User(Base):
    __tablename__ = "users"

    
    id_user = Column(Integer, Sequence('user_id_seq'), name='id_user', primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    token = Column(String)
    mail = Column(String)
    celular = Column(String)
class Group(Base):
    __tablename__ = "groups"
    
    id_group = Column(Integer, Sequence('group_id_seq'), name='id_group', primary_key=True, index=True)
    name = Column(String)
    members_count = Column(Integer)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
class CategoryShare(Base):
    __tablename__ = "categoryShares"
     
    id_cs = Column(Integer, Sequence('cs_id_seq'), name='id_cs', primary_key=True, index=True)
    id_group = Column(Integer, ForeignKey('groups.id_group'), name='id_group')
    id_user = Column(Integer, ForeignKey('users.id_user'), name='id_user')
    category_name = Column(String)
    share_percentage = Column(Integer)


class GroupMember(Base):
    __tablename__ = "groupMembers"
      
    id_gm = Column(Integer, Sequence('gm_id_seq'), name='id_gm', primary_key=True, index=True)
    id_group = Column(Integer, ForeignKey('groups.id_group'),name='id_group')
    id_user = Column(Integer, ForeignKey('users.id_user'),name='id_user')
    is_admin = Column(Boolean)

