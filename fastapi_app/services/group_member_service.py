from sqlalchemy.orm import Session
from fastapi_app import schemas, models


def get_group_members(
    db: Session,
    skip: int, 
    limit: int, 
    id_group: int,
    id_user: int, 
    is_admin: bool
):    
    query = db.query(schemas.GroupMember)

    if id_group is not None:
        query = query.filter_by(id_group=id_group)

    if id_user is not None:
        query = query.filter_by(id_user=id_user)

    if is_admin is not None:
        query = query.filter_by(is_admin=is_admin)

    groupMembers = query.offset(skip).limit(limit).all()
    
    return [
        models.GroupMember(
            id_group=gm.id_group,
            id_user=gm.id_user,
            is_admin=gm.is_admin,
        ) 

        for gm in groupMembers
    ]
    
def create_group_member(db: Session, group_member: models.GroupMember):
    
    db_group_member = schemas.GroupMember(
        id_group=group_member.id_group,
	    id_user=group_member.id_user,
        is_admin=group_member.is_admin,
    )
    group = db.query(schemas.Group).filter_by(id_group=group_member.id_group).first()
    if group is None: 
         raise KeyError("group_id not found: Group does not exist")
    
    user = db.query(schemas.User).filter_by(id_user=group_member.id_user).first()
    if user is None: 
         raise KeyError("user_id not found: User does not exist")
    group.members_count += 1
    
    db.add(db_group_member)
    db.commit()
    db.refresh(db_group_member)
    
    return db_group_member
""" 
def update_group_member(db: Session, group_member_id: int, updated_group_member: models.GroupMember):
    db_group_member = db.query(schemas.GroupMember).filter_by(id=group_member_id).first()
    if db_group_member:
        db_group_member.id_group = updated_group_member.id_group
        db_group_member.id_user = updated_group_member.id_user
        db_group_member.is_admin = updated_group_member.is_admin
        db.commit()
        db.refresh(db_group_member)
        return db_group_member
    return None
 """
def delete_group_member(db: Session, group_member_id: int):
    db_group_member = db.query(schemas.GroupMember).filter_by(id_gm=group_member_id).first()
    if db_group_member:
        db.delete(db_group_member)
        db.commit()
        return True
    return False
