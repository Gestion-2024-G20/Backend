from sqlalchemy import Column, Float, String, Integer, Sequence,  DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
import datetime




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
    password = Column(String)
    token = Column(String)
    mail = Column(String)
    celular = Column(String)
    #foto_perfil = Column()

    