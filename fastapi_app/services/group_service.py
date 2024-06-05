from sqlalchemy.orm import Session
from fastapi_app import schemas, models


def get_groups(
    db: Session,
    skip: int, 
    limit: int, 
    id_group: int,
    name: str, 
    members_count: int, 
    time_created: str
):    
    query = db.query(schemas.Group)

    if id_group is not None:
        query = query.filter_by(id_group=id_group)

    if name is not None:
        query = query.filter_by(name=name)

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


def get_group_by_id(
    db: Session,
    id_group: int,
):    
    group = db.query(schemas.Group).filter_by(id_group=id_group).first()

    
    return models.Group(
            id_group=group.id_group,
            name=group.name,
            members_count=group.members_count,
            time_created=group.time_created.strftime('%Y-%m-%d %H:%M:%S'),
            description=group.description
        ) 
    
    

def create_group(db: Session, group: models.GroupBase):
    
    db_group = schemas.Group(
        name=group.name,
	    members_count= group.members_count,
        description = group.description
    )
    
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    
    return db_group

def update_group(db: Session, group_id: int, updated_group: models.GroupBase):
    db_group = db.query(schemas.Group).filter_by(id_group=group_id).first()
    if db_group:
        db_group.name = updated_group.name
        db_group.members_count = updated_group.members_count
        db.group.description = update_group.description
        db.commit()
        db.refresh(db_group)
        return db_group
    return None

def delete_group(db: Session, group_id: int):
    db_group = db.query(schemas.Group).filter_by(id_group=group_id).first()
    if db_group:

        db_group_member = db.query(schemas.GroupMember).filter_by(id_group=group_id).all()
        if db_group_member:
            for gm in db_group_member:
                db.delete(gm)
                db.commit()

        db_invitations = db.query(schemas.Invitation).filter_by(id_group=group_id).all()
        if db_invitations:
            for i in db_invitations:
                db.delete(i)
                db.commit()

        db_balance = db.query(schemas.Balance).filter_by(id_group=group_id).all()
        if db_balance:
            for b in db_balance:
                db.delete(b)
                db.commit()

        db_request = db.query(schemas.Request).filter_by(id_group=group_id).all()
        if db_request:
            for r in db_request:
                db.delete(r)
                db.commit()
        

        db_categories = db.query(schemas.Category).filter_by(id_group=group_id).all()
        if db_categories:  
            for c in db_categories:
                db_category_shares = db.query(schemas.CategoryShare).filter_by(id_category=c.id_category).all()
                if db_category_shares:  
                    for cs in db_category_shares:
                        db.delete(cs)
                        db.commit()
                db.delete(c)
                db.commit()

        db_expenditures = db.query(schemas.Expenditure).filter_by(id_group=group_id).all()
        if db_expenditures:  
            for e in db_expenditures:
                db_expenditure_shares = db.query(schemas.ExpenditureShare).filter_by(id_expenditure=e.id_expenditure).all()
                if db_expenditure_shares:  
                    for es in db_expenditure_shares:
                        db.delete(es)
                        db.commit()
                db.delete(e)
                db.commit()

        db.delete(db_group)
        db.commit()
        return True
    return False
