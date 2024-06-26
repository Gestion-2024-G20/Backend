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
        is_request=invitation.is_request
    )
    db.add(db_invitation)
    db.commit()
    db.refresh(db_invitation)
    
    return db_invitation


#Obtener una invitacion por su id
def get_invitation(db: Session, invitation_id: int):
    return db.query(schemas.Invitation).filter_by(id_invitation=invitation_id).first()

#obtener invitaciones por id de usuario
def get_invitations_by_user_id(db: Session, user_id: int, is_request: bool):
    query = db.query(
        schemas.Invitation.id_invitation,
        schemas.Invitation.id_group,
        schemas.Invitation.id_user,
        schemas.Invitation.is_request,
        schemas.Group.name.label('group_name')
    ).join(
        schemas.Group, schemas.Invitation.id_group == schemas.Group.id_group
    ).filter(
        schemas.Invitation.id_user == user_id
    )

    if is_request is None or not is_request:
        query = query.filter(schemas.Invitation.is_request == False)
    else:
        query = query.filter(schemas.Invitation.is_request == True)

    results = query.all()
    invitations = []
    for result in results:
        invitation = {
            'id_invitation': result.id_invitation,
            'id_group': result.id_group,
            'id_user': result.id_user,
            'is_request': result.is_request,
            'group_name': result.group_name
        }
        invitations.append(invitation)

    return invitations

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
def get_invitations_by_group_id(db: Session, group_id: int, is_request: bool):
    if is_request is None or is_request != True:
        return db.query(schemas.Invitation).filter_by(id_group=group_id).all()
    return db.query(schemas.Invitation).filter_by(id_group=group_id, is_request = True).all()


def get_users_by_invitations(db: Session, invitations: List[models.Invitation]):
    print("Entré acá")
    users = []
    for invitation in invitations:
        user = db.query(schemas.User).filter_by(id_user=invitation.id_user).first()

        users.append(user)
    return users

def get_requested_invitations_by_group_id(db: Session, group_id: int):
    return db.query(schemas.Invitation).filter_by(group_id=group_id, is_request=True).all()