from pyparsing import List
from sqlalchemy.orm import Session
from fastapi_app import schemas, models

def create_request_url(db: Session, request: models.Request):
    print("creating request")
    print(request)
    group = db.query(schemas.Group).filter_by(id_group=request.id_group).first()
    if group is None: 
        raise KeyError("group_id not found: Group does not exist")
            
    db_request = schemas.Request(
        id_group=request.id_group,
        token=request.token
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    
    return db_request

def find_valid_request(db: Session, request: models.Request):
    db_request = db.query(schemas.Request).filter_by(id_group=request.id_group, token=request.token).first()
    return db_request

def get_request_by_user_id_to_group(db: Session, user_id: int, group_id: int):
    return db.query(schemas.Invitation).filter_by(id_user=user_id, id_group=group_id, is_request = True).first()
