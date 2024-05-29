from uuid import uuid4
from sqlalchemy.orm import Session
from sqlalchemy import update
from fastapi_app.schemas import ExpenditureShare
from fastapi_app.services.balance_service import add_expenditure_share_to_balance

def create_expenditure_share(db: Session, expenditure_share: ExpenditureShare):
    db_expenditure_share = ExpenditureShare(
        id_expenditure=expenditure_share.id_expenditure,
        id_user=expenditure_share.id_user,
        share_percentage=expenditure_share.share_percentage
    )
    db.add(db_expenditure_share)
    db.commit()
    db.refresh(db_expenditure_share)

    add_expenditure_share_to_balance(db, expenditure_share=expenditure_share)

    return db_expenditure_share

def get_expenditure_shares(
    db: Session, id_expenditure: int, id_user: int = None,
    skip: int = 0, limit: int = 100
):
    query = db.query(
        ExpenditureShare
    )
    if id_expenditure is not None:
        query = query.filter_by(id_expenditure=id_expenditure)
        
    if id_user is not None:
        query = query.filter_by(id_user=id_user)

    expenditure_shares = query.offset(skip).limit(limit).all()

    return [
        ExpenditureShare(
            id_user=es.id_user,
            id_expenditure=es.id_expenditure,
            share_percentage=es.share_percentage
        ) 

        for es in expenditure_shares
    ]

def update_expenditure_share(db: Session, expenditure_share_id: int, updated_expenditure_share: ExpenditureShare):
    db_expenditure_share = db.query(ExpenditureShare).filter_by(id_es=expenditure_share_id).first()
    if db_expenditure_share:
        update_query = update(ExpenditureShare).where(ExpenditureShare.id_es == expenditure_share_id
        ).values(
            {
             ExpenditureShare.id_expenditure: updated_expenditure_share.id_expenditure,
             ExpenditureShare.id_user: updated_expenditure_share.id_user,
             ExpenditureShare.share_percentage: updated_expenditure_share.share_percentage,
            }
        )
        db.execute(update_query)
        db.commit()

        db.refresh(db_expenditure_share)        
    
        add_expenditure_share_to_balance(db, expenditure_share=updated_expenditure_share)

        return db_expenditure_share
    return None

def delete_expenditure_share(db: Session, expenditure_share_id: int):
    db_expenditure_share = db.query(ExpenditureShare).filter_by(id_es=expenditure_share_id).first()
    if db_expenditure_share: 
        for es in db_expenditure_share:
            db.delete(es)
        db.commit()
        return True
    return False

def delete_expenditure_share_by_expenditure_id(db: Session, expenditure_id: int):
    db_expenditure_shares = db.query(ExpenditureShare).filter_by(id_expenditure=expenditure_id).all()
    for db_expenditure_share in db_expenditure_shares:
        db.delete(db_expenditure_share)
        db.commit()
    
    return db_expenditure_shares
    
