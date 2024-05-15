from sqlalchemy.orm import Session
from fastapi_app import schemas, models


def create_user(db: Session, user: models.User):

    db_user = schemas.User(
        username=user.username,
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
    id_user: int = None, 
    username: str = None,

):
    query = db.query(schemas.User)

    if id_user is not None:
        query = query.filter_by(id_user=id_user)

    if username is not None:
        query = query.filter_by(username=username)

    users = query.offset(skip).limit(limit).all()

    return [
        models.User(
            id_user=u.id_user,
            username=u.username, 
            password=u.password,
            token=u.token,
            mail=u.mail,
            celular=u.celular
        ) 

        for u in users
    ]

def get_user(
    db: Session, 
    id_user: int,
):
    query = db.query(schemas.User).filter_by(id_user=id_user)
    user = query.first()
    if user:
        return models.User(
            id_user=user.id_user,
            username=user.username, 
            password=user.password,
            token=user.token,
            mail=user.mail,
            celular=user.celular
        )
    else:
        return None

def update_user(db: Session, user_id: int, updated_user: models.User):
    db_user = db.query(schemas.User).filter_by(id_user=user_id).first()
    if db_user:
        db_user.username = updated_user.username
        db_user.password = updated_user.password
        db_user.token = updated_user.token
        db_user.mail = updated_user.mail
        db_user.celular = updated_user.celular
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

def delete_user(db: Session, user_id: int):
    db_user = db.query(schemas.User).filter_by(id_user=user_id).first()
    if db_user:

        db_group_member = db.query(schemas.GroupMember).filter_by(id_user=user_id).all()
        if db_group_member:
            for gm in db_group_member:
                db.delete(gm)

        db_category_share = db.query(schemas.CategoryShare).filter_by(id_user=user_id).first()
        if db_category_share:
            for cs in db_category_share:
                db.delete(cs)

        db.delete(db_user)
        db.commit()
        return True
    return False
