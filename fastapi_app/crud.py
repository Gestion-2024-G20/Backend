from uuid import uuid4
from sqlalchemy.orm import Session

import schemas
from models import Expenditure, User

def create_expenditure(db: Session, expenditure: schemas.ExpenditureBase):
    db_expenditure = Expenditure(
        id_user=expenditure.id_user,
        amount=expenditure.amount,
        id_group=expenditure.id_group,
        description=expenditure.description
    )
    db.add(db_expenditure)
    db.commit()
    db.refresh(db_expenditure)

    return db_expenditure


def get_expenditures(
    db: Session, id_group: int, id_user: int = None,
    skip: int = 0, limit: int = 100
):
    query = db.query(
    	Expenditure.id_user,
    	Expenditure.amount,
    	Expenditure.id_group, 
    	Expenditure.description, 
    	Expenditure.time_created
    ).filter_by(id_group=id_group)

    if id_user is not None:
        query = query.filter_by(id_user=id_user)

    expenditures = query.offset(skip).limit(limit).all()

    return [
        schemas.Expenditure(
            id_user=e.id_user,
            amount=e.amount,
            id_group=e.id_group,
            description=e.description,
            time_created=e.time_created.strftime('%Y-%m-%d %H:%M:%S')
        ) 

        for e in expenditures
    ]

def create_user(db: Session, user: schemas.UserBase):
    db_user = User(
        id_user=user.id_user,
        password=user.password,
        token=user.token,
        mail=user.mail,
        celular=user.celular
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_users(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    id_user: int = None
):
    query = db.query(
    	User.id_user,
    	User.password,
    	User.token, 
    	User.mail, 
    	User.celular
    )

    if id_user is not None:
        query = query.filter_by(id_user=id_user)

    users = query.offset(skip).limit(limit).all()

    return [
        schemas.User(
            id_user=u.id_user,
            password=u.password,
            token=u.token,
            mail=u.mail,
            celular=u.celular
        ) 

        for u in users
    ]

    


