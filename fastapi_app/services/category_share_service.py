from sqlalchemy.orm import Session
from fastapi_app import schemas, models


def get_category_shares(
    db: Session,
    skip: int, 
    limit: int, 
    id_cs: int,
    id_group: int,
    id_user: int, 
    category_name: str, 
    share_percentage: int
):    
    query = db.query(schemas.CategoryShare)

    if id_cs is not None:
        query = query.filter_by(id_cs=id_cs)

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
        models.CategoryShare(
            id_cs=cs.id_cs,
            id_group=cs.id_group,
            id_user=cs.id_user,
            category_name=cs.category_name,
            share_percentage=cs.share_percentage
        ) 

        for cs in category_shares
    ]
        
def create_category_share(db: Session, category_share: models.CategoryShare):
    
    db_category_share = schemas.CategoryShare(
            id_group=category_share.id_group,
            id_user=category_share.id_user,
            category_name=category_share.category_name,
            share_percentage=category_share.share_percentage
    )
    group = db.query(schemas.Group).filter_by(id_group=category_share.id_group).first()
    if group is None: 
         raise KeyError("group_id not found: Group does not exist")
    
    user = db.query(schemas.User).filter_by(id_user=category_share.id_user).first()
    if user is None: 
         raise KeyError("user_id not found: User does not exist")
    group.members_count += 1
    db.add(db_category_share)
    db.commit()
    db.refresh(db_category_share)
    
    return db_category_share
""" 
def update_category_share(db: Session, category_share_id: int, updated_category_share: models.CategoryShare):
    db_category_share = db.query(schemas.CategoryShare).filter_by(id=category_share_id).first()
    if db_category_share:
        db_category_share.id_group = updated_category_share.id_group
        db_category_share.id_user = updated_category_share.id_user
        db_category_share.category_name = updated_category_share.category_name
        db_category_share.share_percentage = updated_category_share.share_percentage
        db.commit()
        db.refresh(db_category_share)
        return db_category_share
    return None
"""
def delete_category_share(db: Session, category_share_id: int):
    db_category_share = db.query(schemas.CategoryShare).filter_by(id_cs=category_share_id).first()
    if db_category_share:
        db.delete(db_category_share)
        db.commit()
        return True
    return False
