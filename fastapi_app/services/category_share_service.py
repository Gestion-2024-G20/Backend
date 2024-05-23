from sqlalchemy.orm import Session
from fastapi_app import schemas, models
from ..schemas import Category, CategoryShare

def get_category_shares(
    db: Session,
    skip: int, 
    limit: int, 
    id_cs: int,
    id_category: int,
    id_user: int, 
    share_percentage: int
):    
    query = db.query(schemas.CategoryShare)

    if id_cs is not None:
        query = query.filter_by(id_cs=id_cs)

    if id_category is not None:
        query = query.filter_by(id_category=id_category)

    if id_user is not None:
        query = query.filter_by(id_user=id_user)

    if share_percentage is not None:
        query = query.filter_by(share_percentage=share_percentage)

    category_shares = query.offset(skip).limit(limit).all()
    
    return [
        models.CategoryShare(
            id_cs=cs.id_cs,
            id_category=cs.id_category,
            id_user=cs.id_user,
            share_percentage=cs.share_percentage
        ) 

        for cs in category_shares
    ]
     
def get_group_category_shares(
    db: Session,
    id_group: int, 
):    
    inner_join = db.query(Category, CategoryShare).filter_by(id_group=id_group).join(CategoryShare, Category.id_category==CategoryShare.id_category).all()

    
    return [
        models.CategoryShare(
            id_cs=cs.id_cs,
            id_category=cs.id_category,
            id_user=cs.id_user,
            share_percentage=cs.share_percentage
        ) 

        for cs in inner_join
    ]
        
def create_category_share(db: Session, category_share: models.CategoryShare):
    
    db_category_share = schemas.CategoryShare(
            id_category=category_share.id_category,
            id_user=category_share.id_user,
            share_percentage=category_share.share_percentage
    )
    category = db.query(schemas.Category).filter_by(id_category=category_share.id_category).first()
    if category is None: 
         raise KeyError("category_id not found: Category does not exist")
    
    user = db.query(schemas.User).filter_by(id_user=category_share.id_user).first()
    if user is None: 
         raise KeyError("user_id not found: User does not exist")
    
    db.add(db_category_share)
    db.commit()
    db.refresh(db_category_share)
    
    return db_category_share

def update_category_share(db: Session, category_share_id: int, updated_category_share: models.CategoryShare):
    db_category_share = db.query(schemas.CategoryShare).filter_by(id=category_share_id).first()
    if db_category_share:
        db_category_share.id_category = updated_category_share.id_category
        db_category_share.id_user = updated_category_share.id_user
        db_category_share.share_percentage = updated_category_share.share_percentage
        db.commit()
        db.refresh(db_category_share)
        return db_category_share
    return None

def delete_category_share(db: Session, category_share_id: int):
    db_category_share = db.query(schemas.CategoryShare).filter_by(id_cs=category_share_id).first()
    if db_category_share:
        db.delete(db_category_share)
        db.commit()
        return True
    return False

def delete_category_category_shares(db: Session, category_id: int):
    db_category_shares = db.query(schemas.CategoryShare).filter_by(id_category=category_id).all()
    if db_category_shares and db_category_shares:
        for cs in db_category_shares: 
            db.delete(cs)
        db.commit()
        return db_category_shares
    return False
