from ast import alias
from uuid import uuid4
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, update
from sqlalchemy.orm import aliased
from fastapi_app.models import ExpenditureBase, ExpenditureComplete
from fastapi_app.schemas import Expenditure, Category, User
from fastapi_app.services.balance_service import delete_expenditure_from_balance, add_expenditure_to_balance
from fastapi_app.services.expenditure_share_service import delete_expenditure_share_by_expenditure_id

def create_expenditure(db: Session, expenditure: ExpenditureBase):
    db_expenditure = Expenditure(
        id_user=expenditure.id_user,
        amount=expenditure.amount,
        id_group=expenditure.id_group,
        description=expenditure.description,
        id_category=expenditure.id_category
    )
    db.add(db_expenditure)
    db.commit()
    db.refresh(db_expenditure)

    return db_expenditure


def get_expenditures(
    db: Session, id_group: int = None, id_user: int = None, id_expenditure: int = None,
    skip: int = 0, limit: int = 100
):
    query = db.query(
    	Expenditure
    )

    if id_expenditure is not None:
        query = query.filter_by(id_expenditure=id_expenditure)
    
    if id_group is not None:
        query = query.filter_by(id_group=id_group)

    if id_user is not None:
        query = query.filter_by(id_user=id_user)

    expenditures = query.offset(skip).limit(limit).all()

    return [
        Expenditure(
            id_user=e.id_user,
            amount=e.amount,
            id_group=e.id_group,
            description=e.description,
            id_category=e.id_category,
            time_created=e.time_created.strftime('%Y-%m-%d %H:%M:%S')
        ) 

        for e in expenditures
    ]
def get_group_expenditures(
    db: Session, id_group: int,
    id_user: int = None, id_category: int = None,
    min_date: str = None, max_date: str = None
):

    query = db.query(
        Expenditure, Category, User.username
    ).join(
        Category, Expenditure.id_category == Category.id_category
    ).join(
        User, Expenditure.id_user == User.id_user
    ).filter(
        Expenditure.id_group == id_group
    )
	
    if id_user is not None:
        query = query.filter(Expenditure.id_user == id_user)

    if id_category is not None:
        query = query.filter(Expenditure.id_category == id_category)

    if min_date is not None:
        query = query.filter(func.date(Expenditure.time_created) >= min_date)

    if max_date is not None:
        query = query.filter(func.date(Expenditure.time_created) <= max_date)
    
    expenditures = query.all()

    return [
        ExpenditureComplete(
            id_user=e.id_user,
            amount=e.amount,
            id_group=e.id_group,
            description=e.description,
            id_category=e.id_category,
            name_category=(c.name if c else "SALDO DEUDA"),
            username=u.username,
            time_created=e.time_created.strftime('%Y-%m-%d %H:%M:%S'), 
            id_expenditure=e.id_expenditure,
        ) 

        for e, c, u in expenditures
    ]


def update_expenditure(db: Session, expenditure_id: int, updated_expenditure: ExpenditureBase):
    db_expenditure = db.query(Expenditure).filter_by(id_expenditure=expenditure_id).first()
    if db_expenditure:
        delete_expenditure_from_balance(db=db, id_expenditure=expenditure_id)
        update_query = update(Expenditure).where(Expenditure.id_expenditure==expenditure_id
        ).values(
            {
             Expenditure.amount: updated_expenditure.amount,
             Expenditure.description: updated_expenditure.description,
             Expenditure.id_category: updated_expenditure.id_category,
            }
        )
        db.execute(update_query)
        db.commit()

        db.refresh(db_expenditure)
        return db_expenditure
    return None




def delete_expenditure(db: Session, expenditure_id: int):
    db_expenditure = db.query(Expenditure).filter_by(id_expenditure=expenditure_id).first()
    if db_expenditure:
        delete_expenditure_from_balance(db, expenditure_id)
        delete_expenditure_share_by_expenditure_id(db, expenditure_id=expenditure_id)

        db.delete(db_expenditure)
        db.commit()
        return True
    return False