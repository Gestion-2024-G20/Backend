
from sqlalchemy import Boolean, Column, Float, ForeignKey, ForeignKeyConstraint, String, Integer, Sequence,  DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import UniqueConstraint

Base = declarative_base()

class Expenditure(Base):
    __tablename__ = "expenditures"
    
    id_user = Column(Integer, ForeignKey('users.id_user'))
    amount =  Column(Float)
    id_group = Column(Integer, ForeignKey('groups.id_group'))
    id_category = Column(Integer, ForeignKey('categories.id_category'))
    description = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    id_expenditure = Column(Integer, Sequence('expenditure_id_seq'), primary_key=True, index=True)

class User(Base):
    __tablename__ = "users"
    
    id_user = Column(Integer, Sequence('user_id_seq'), name='id_user', primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    name = Column(String)
    lastname = Column(String)
    token = Column(String)
    mail = Column(String)
    celular = Column(String)
    profile_image_name = Column(String(255), nullable=True)



class Group(Base):
    __tablename__ = "groups"
    
    id_group = Column(Integer, Sequence('group_id_seq'), name='id_group', primary_key=True, index=True)
    name = Column(String)
    members_count = Column(Integer)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    description = Column(String)
    is_deleted = Column(Boolean)
    
class Category(Base):
    __tablename__ = "categories"
    
    id_category = Column(Integer, Sequence('category_id_seq'), name='id_category', primary_key=True, index=True)
    id_group = Column(Integer, ForeignKey('groups.id_group'))
    name = Column(String)
    description = Column(String)

    __table_args__ = (UniqueConstraint('id_group', 'name', name='_group_name_uc'),)


class CategoryShare(Base):
    __tablename__ = "categoryShares"
     
    id_cs = Column(Integer, Sequence('cs_id_seq'), name='id_cs', primary_key=True, index=True)
    id_category = Column(Integer, ForeignKey('categories.id_category'), name='id_category')
    id_user = Column(Integer, ForeignKey('users.id_user'), name='id_user')
    share_percentage = Column(Integer)

class ExpenditureShare(Base):
    __tablename__ = "expenditureShares"

    id_es = Column(Integer, Sequence('es_id_seq'), name='id_es', primary_key=True, index=True) 
    id_expenditure = Column(Integer, ForeignKey('expenditures.id_expenditure'), name='id_expenditure')
    id_user = Column(Integer, ForeignKey('users.id_user'), name='id_user')
    share_percentage = Column(Integer)
class GroupMember(Base):
    __tablename__ = "groupMembers"
      
    id_gm = Column(Integer, Sequence('gm_id_seq'), name='id_gm', primary_key=True, index=True)
    id_group = Column(Integer, ForeignKey('groups.id_group'),name='id_group')
    id_user = Column(Integer, ForeignKey('users.id_user'),name='id_user')
    is_admin = Column(Boolean)

#Tabla de Invitaciones
class Invitation(Base):
    __tablename__ = "invitations"
     
    id_invitation = Column(Integer, Sequence('invitation_id_seq'), name='id_invitation', primary_key=True, index=True)
    id_group = Column(Integer, ForeignKey('groups.id_group'), name='id_group')
    id_user = Column(Integer, ForeignKey('users.id_user'), name='id_user')
    is_request = Column(Boolean)


# Tabla de saldos
class Balance(Base):
    __tablename__ = "balance"

    id_user_1 = Column(Integer, ForeignKey('users.id_user'), name='id_user_1', primary_key=True, index=True)
    id_user_2 = Column(Integer, ForeignKey('users.id_user'), name='id_user_2', primary_key=True, index=True)
    id_group = Column(Integer, ForeignKey('groups.id_group'), name='id_group', primary_key=True, index=True)
    balance = Column(Float)

#Tabla de solicitudes
class Request(Base):
    __tablename__ = "requests"
     
    id_request = Column(Integer, Sequence('request_id_seq'), name='id_request', primary_key=True, index=True)
    id_group = Column(Integer, ForeignKey('groups.id_group'), name='id_group')
    token = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())