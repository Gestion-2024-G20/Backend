from uuid import uuid4
from sqlalchemy.orm import Session
from fastapi_app.schemas import ExpenditureShare

def create_expenditure_share(db: Session, expenditure_share: ExpenditureShare):
    db_expenditure_share = ExpenditureShare(
        id_expenditure=expenditure_share.id_expenditure,
        id_user=expenditure_share.id_user,
        share_percentage=expenditure_share.share_percentage
    )
    db.add(db_expenditure_share)
    db.commit()
    db.refresh(db_expenditure_share)

    return db_expenditure_share

def get_expenditure_shares(
    db: Session, id_group: int, id_user: int = None,
    skip: int = 0, limit: int = 100
):
    query = db.query(
        ExpenditureShare()
    ).filter_by(id_group=id_group)

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
        db_expenditure_share.id_expenditure = updated_expenditure_share.id_expenditure
        db_expenditure_share.id_user = updated_expenditure_share.id_user
        db_expenditure_share.share_percentage = updated_expenditure_share.share_percentage
        db.commit()
        db.refresh(db_expenditure_share)
        return db_expenditure_share
    return None

def delete_expenditure_share(db: Session, expenditure_share_id: int):
    db_expenditure_share = db.query(ExpenditureShare).filter_by(id_es=expenditure_share_id).first()
    if db_expenditure_share:
        db.delete(db_expenditure_share)
        db.commit()
        return True
    return False
