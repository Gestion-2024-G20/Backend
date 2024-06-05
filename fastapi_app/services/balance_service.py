from sqlalchemy.orm import Session
from fastapi_app import schemas, models
from sqlalchemy import and_, or_, update
from typing import Optional


def get_balance(
    db: Session,
    id_group: int,
    id_user: int, 
):    
    query = db.query(schemas.Balance).filter_by(id_group=id_group)

    query_to_pay = query.filter(or_(
        and_(schemas.Balance.id_user_1 == id_user, schemas.Balance.balance < 0),
        and_(schemas.Balance.id_user_2 == id_user, schemas.Balance.balance > 0)
    ))

    balance_to_pay = get_balance_items(db, query_to_pay, id_user)
    
    query_to_receive = query.filter(or_(
        and_(schemas.Balance.id_user_1 == id_user, schemas.Balance.balance > 0),
        and_(schemas.Balance.id_user_2 == id_user, schemas.Balance.balance < 0)
    ))

    balance_to_receive = get_balance_items(db, query_to_receive, id_user)

    return models.Balance(
            to_pay=balance_to_pay,
            to_receive=balance_to_receive
        ) 

def is_null(db: Session,
            id_group: int):
    query = db.query(schemas.Balance.balance).filter_by(id_group=id_group).filter(schemas.Balance.balance != 0)
    count = query.count()

    if count == 0:
        return 1
    else:
        return 0


def get_balance_items(db, query, id_user):
    from fastapi_app.services.user_service import get_user
    balance_items = []
    for b in query.all():
        if b.id_user_1 != id_user:
            id_other_user = b.id_user_1 
        else: 
            id_other_user = b.id_user_2

        username = get_user(db, id_other_user).username

        balance = abs(b.balance)

        balance_item = models.BalanceItem(
            id_user= id_other_user,
            amount=balance,
            username=username
        )

        balance_items.append(balance_item)

    return balance_items

# Obtener todos los miembros del grupo (menos el actual)
def get_group_members(
        db: Session,
        id_group: int,
        id_user: int
):
    # Evitar import circular
    from fastapi_app.services.group_member_service import get_group_members
    group_members = get_group_members(db,skip=None,limit=None, id_group=id_group, id_user=None, is_admin=None)
    return [g for g in group_members  if g.id_user != id_user]


# Crear balance con los otros miembros del grupo
def create_balance(
            db: Session,
            group_member: models.GroupMember
 ):
    group_members = get_group_members(db, group_member.id_group, group_member.id_user)
    for g in group_members:
        db_balance = schemas.Balance(
            id_user_1 = group_member.id_user,
            id_user_2 = g.id_user,
            id_group = g.id_group,
            balance = 0
        )
        db.add(db_balance)
        db.commit()
        db.refresh(db_balance)

def add_expenditure_to_balance(
        db: Session,
        expenditure: models.ExpenditureBase
):
    from fastapi_app.services.expenditure_share_service import get_expenditure_shares
    expenditure_shares = get_expenditure_shares(db, id_expenditure=expenditure.id_expenditure) 
    for expenditure_share in expenditure_shares:
        
        if expenditure_share.id_user == expenditure.id_user:
            continue

        add_expenditure_share_to_balance(db, expenditure=expenditure, expenditure_share=expenditure_share)


def delete_expenditure_from_balance(
        db: Session,
        id_expenditure: int
):
    from fastapi_app.services.expenditure_service import get_expenditures
    expenditure = get_expenditures(db, id_expenditure=id_expenditure)[0]

    inverse_expenditure = models.ExpenditureBase(
        id_user=expenditure.id_user,
        amount= - expenditure.amount,
        id_expenditure=id_expenditure,
        id_group=expenditure.id_group,
        id_category=expenditure.id_category,
        description=expenditure.description
    )
    add_expenditure_to_balance(db, inverse_expenditure)
  
def add_expenditure_share_to_balance(
    db: Session,
    expenditure_share: models.ExpenditureShare,
    expenditure: Optional[models.ExpenditureBase] = None,
):
    if expenditure is None:
        from fastapi_app.services.expenditure_service import get_expenditures
        expenditure = get_expenditures(db, id_expenditure=expenditure_share.id_expenditure)[0]

    if expenditure_share.id_user == expenditure.id_user:
        return
        
    # El monto de lo que le debe cada uno de los otros usuario por el nuevo gasto
    new_debt_amount = expenditure.amount * expenditure_share.share_percentage / 100
    if new_debt_amount == 0:
        return

    # Si el id_user_1 es el del otro, eso signfica que tengo que restar del balance
    update1 = update(schemas.Balance).where(and_(
            schemas.Balance.id_group==expenditure.id_group,
            schemas.Balance.id_user_1==expenditure_share.id_user,
            schemas.Balance.id_user_2==expenditure.id_user
    )).values(
            {
             schemas.Balance.balance:  schemas.Balance.balance - new_debt_amount
            }
    )
    db.execute(update1)
    db.commit()

    # Si el id_user_1 es el de la persona que hizo el gasto, eso signfica que tengo que sumar del balance
    update2 = update(schemas.Balance).where(and_(
            schemas.Balance.id_group==expenditure.id_group,
            schemas.Balance.id_user_1==expenditure.id_user,
            schemas.Balance.id_user_2==expenditure_share.id_user
    )).values(
            {
             schemas.Balance.balance:  schemas.Balance.balance + new_debt_amount
            }
    )
    db.execute(update2)
    db.commit()

        
