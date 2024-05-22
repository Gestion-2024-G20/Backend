from pyparsing import List
from sqlalchemy.orm import Session
from fastapi_app import schemas, models

# Crear una invitación
def create_invitation(db: Session, invitation: models.Invitation):
    print("creating invitation")
    print(invitation)
    print(invitation.id_group)
    # print("group_id: ", invitation.group_id, " user_id: ", invitation.user_id)
    group = db.query(schemas.Group).filter_by(id_group=invitation.id_group).first()
    if group is None: 
        raise KeyError("group_id not found: Group does not exist")
    
    user = db.query(schemas.User).filter_by(id_user=invitation.id_user).first()
    if user is None: 
        raise KeyError("user_id not found: User does not exist")
    
    db_invitation = schemas.Invitation(
        id_group=invitation.id_group,
        id_user=invitation.id_user,
    )
    db.add(db_invitation)
    db.commit()
    db.refresh(db_invitation)
    
    return db_invitation


#Obtener una invitacion por su id
def get_invitation(db: Session, invitation_id: int):
    return db.query(schemas.Invitation).filter_by(id_invitation=invitation_id).first()

#obtener invitaciones por id de usuario
def get_invitations_by_user_id(db: Session, user_id: int):
    return db.query(schemas.Invitation).filter_by(id_user=user_id).all()

def delete_invitation(db: Session, invitation_id: int):
    print("deleting invitation")
    db_invitation = db.query(schemas.Invitation).filter_by(id_invitation=invitation_id).first()
    if db_invitation:
        db.delete(db_invitation)
        db.commit()
        return True
    return False

def get_invitation_by_user_id_group_id(db: Session, user_id: int, group_id: int):
    return db.query(schemas.Invitation).filter_by(id_user=user_id, id_group=group_id).first()


#Obtener invitaciones por id de grupo
def get_invitations_by_group_id(db: Session, group_id: int):
    return db.query(schemas.Invitation).filter_by(id_group=group_id).all()


def get_users_by_invitations(db: Session, invitations: List[models.Invitation]):
    print("Entré acá")
    users = []
    for invitation in invitations:
        user = db.query(schemas.User).filter_by(id_user=invitation.id_user).first()

        users.append(user)
    return users