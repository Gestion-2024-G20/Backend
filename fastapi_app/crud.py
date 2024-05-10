from uuid import uuid4
from sqlalchemy.orm import Session

import fastapi_app.models as models
from fastapi_app.models import *
from fastapi_app.schemas import *

def create_expenditure(db: Session, expenditure: models.ExpenditureBase):
    db_expenditure = Expenditure(
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
        models.Expenditure(
            id_user=e.id_user,
            amount=e.amount,
            id_group=e.id_group,
            description=e.description,
            time_created=e.time_created.strftime('%Y-%m-%d %H:%M:%S')
        ) 

        for e in expenditures
    ]

def create_user(db: Session, user: models.User):

    db_user = User(
        username= user.username,
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
    query = db.query(
    	User.id_user,
        User.username, 
    	User.password,
    	User.token, 
    	User.mail, 
    	User.celular
    )

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
    username: str,

):
    print("query ")
    query = db.query(
    	User.id_user,
        User.username, 
    	User.password,
    	User.token, 
    	User.mail, 
    	User.celular
    )


    query = query.filter_by(username=username)

    user = query.first()
    if user :

        return models.User(
                id_user=user[0],
                username=user[1], 
                password=user[2],
                token=user[3],
                mail=user[4],
                celular=user[5]
            ) 
    else: 
        return None


def get_groups(
    db: Session,
    skip: int, 
    limit: int, 
    id_group: int,
    members_count: int, 
    time_created: str
):    
    query = db.query(Group)

    if id_group is not None:
        query = query.filter_by(id_group=id_group)

    if members_count is not None:
        query = query.filter_by(members_count=members_count)

    if time_created is not None:
        query = query.filter_by(time_created=time_created)

    groups = query.offset(skip).limit(limit).all()
    
    return [
        models.Group(
            id_group=g.id_group,
            name=g.name,
            members_count=g.members_count,
            time_created=g.time_created.strftime('%Y-%m-%d %H:%M:%S'),
        ) 

        for g in groups
    ]
    
def create_group(db: Session, group: models.Group):
    
    db_group = Group(
        name=group.name,
	    members_count= group.members_count,
        time_created=group.time_created,
    )
    
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    
    return db_group

def get_group_members(
    db: Session,
    skip: int, 
    limit: int, 
    id_group: int,
    id_user: int, 
    is_admin: bool
):    
    query = db.query(GroupMember)

    if id_group is not None:
        query = query.filter_by(id_group=id_group)

    if id_user is not None:
        query = query.filter_by(id_user=id_user)

    if is_admin is not None:
        query = query.filter_by(is_admin=is_admin)

    groupMembers = query.offset(skip).limit(limit).all()
    
    return [
        GroupMember(
            id_group=gm.id_group,
            id_user=gm.id_user,
            is_admin=gm.is_admin,
        ) 

        for gm in groupMembers
    ]
    
def create_group_member(db: Session, group_member: GroupMember):
    
    db_group_member = GroupMember(
        id_group=group_member.id_group,
	    id_user=group_member.id_user,
        is_admin=group_member.is_admin,
    )
    
    db.add(db_group_member)
    db.commit()
    db.refresh(db_group_member)
    
    return db_group_member


def get_category_shares(
    db: Session,
    skip: int, 
    limit: int, 
    id_group: int,
    id_user: int, 
    category_name: str, 
    share_percentage: int
):    
    query = db.query(CategoryShare)

    if id_group is not None:
        query = query.filter_by(id_group=id_group)

    if id_user is not None:
        query = query.filter_by(id_user=id_user)

    if category_name is not None:
        query = query.filter_by(category_name=category_name)

    if share_percentage is not None:
        query = query.filter_by(share_percentage=share_percentage)

    category_shares = query.offset(skip).limit(limit).all()
    
    return [
        CategoryShare(
            id_group=cs.id_group,
            id_user=cs.id_user,
            category_name=cs.category_name,
            share_percentage=cs.share_percentage
        ) 

        for cs in category_shares
    ]
        
def create_category_share(db: Session, category_share: CategoryShare):
    
    db_category_share = CategoryShare(
            id_group=category_share.id_group,
            id_user=category_share.id_user,
            category_name=category_share.category_name,
            share_percentage=category_share.share_percentage
    )
    
    db.add(db_category_share)
    db.commit()
    db.refresh(db_category_share)
    
    return db_category_share
