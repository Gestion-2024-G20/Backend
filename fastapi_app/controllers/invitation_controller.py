from typing import Optional
from fastapi import APIRouter, Depends, Query
from pyparsing import List
from sqlalchemy.orm import Session
from fastapi_app.services import invitation_service
from fastapi_app.get_db import get_db
from fastapi_app.models import Invitation, ResponseModel, User
from fastapi_app.services import group_service
from fastapi_app.services import group_member_service

router = APIRouter()

#Crea una invitación
@router.post("/invitations")
async def create_invitation(invitation: Invitation, db: Session = Depends(get_db)):
    try:
        invitation = invitation_service.create_invitation(db, invitation)
        return ResponseModel(
            code=0,
            message="OK",
            detail="User created successfully",
            dataModel=invitation
        )
    except Exception as e:
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )

#Obtiene una invitación por su id
@router.get("/invitations/{invitation_id}")
async def get_invitation(invitation_id: int, db: Session = Depends(get_db)):
    try:
        invitation = invitation_service.get_invitation(db, invitation_id)
        if invitation is None:
            return ResponseModel(
                code=1,
                message="NOT FOUND",
                detail="Invitation not found",
                dataModel=None
            )
        
        return ResponseModel(
            code=0,
            message="OK",
            detail="Invitation retrieved successfully",
            dataModel=invitation
        )
    except Exception as e:
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )

#Obtiene todas las invitaciones de un usuario
@router.get("/user/{user_id}/userGroupInvitations")
async def get_invitations(user_id: int, db: Session = Depends(get_db), requested: Optional[bool] = Query(None, description="Filtrar por invitaciones solicitadas")):
    try:
        invitations = invitation_service.get_invitations_by_user_id(db, user_id, requested)
        return ResponseModel(
            code=0,
            message="OK",
            detail="Invitations retrieved successfully",
            dataModel=invitations
        )
    except Exception as e:
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )
    
#Eliminar una invitacion dado su id (ya sea porque se aceptó o se rechazó)
@router.delete("/invitations/borrar/{invitation_id}")
async def delete_invitation(invitation_id: int, db: Session = Depends(get_db)):
    try:
        deleted_invitation = invitation_service.delete_invitation(db, invitation_id)
        if not deleted_invitation:
            return ResponseModel(
                code=1,
                message="NOT FOUND",
                detail="Invitation not found",
                dataModel=deleted_invitation #deleted_invitation acá es false
            )
        
        return ResponseModel(
            code=0,
            message="OK",
            detail="Invitation deleted successfully",
            dataModel=deleted_invitation # deleted_invitation acá es true
        )
    except Exception as e:
        return ResponseModel(
            code=1, 
            message="ERROR",
            detail=str(e),
            dataModel=None
        )

#Obtener una invitacion dados su id de usuario y su id de grupo
@router.get("/invitations/{userId}/group/{groupId}", response_model=ResponseModel)
async def get_invitation_by_user_id_group_id(userId: int, groupId: int, db: Session = Depends(get_db)):
    try:
        invitation = invitation_service.get_invitation_by_user_id_group_id(db, userId, groupId)
        #Si no existía ninguna invitación, está todo joya
        if invitation:
            return ResponseModel(
                code=0,
                message="OK",
                detail="Invitation retrieved successfully",
                dataModel=invitation
            )
        
        return ResponseModel(
            code=1,
            message="ERROR",
            detail="The invitation does not exist",
            dataModel=[]
        )

    
    except Exception as e:
        return ResponseModel(
            code=1, 
            message="ERROR",
            detail=str(e),
            dataModel=None
        )

#Obtener las invitaciones de un grupo dado su id
@router.get("/invitations/group/{groupId}", response_model=ResponseModel)
async def get_invitations_by_group_id(groupId: int, db: Session = Depends(get_db)):
    try:
        invitations = invitation_service.get_invitations_by_group_id(db, groupId, None)
        print(invitations)  
        if not invitations:
            return ResponseModel(
                code=1,
                message="NOT FOUND",
                detail="No invitations found for this group",
                dataModel=[]
            )
        return ResponseModel(
            code=0,
            message="OK",
            detail="Invitations retrieved successfully",
            dataModel=invitations
        )
    except Exception as e:
        return ResponseModel(
            code=1, 
            message="ERROR",
            detail=str(e),
            dataModel=None
        )
    


@router.get("/invitations/users/{id_group}", response_model=ResponseModel)
async def get_users_by_invitation_group_id(id_group: int, db: Session = Depends(get_db), requested: Optional[bool] = Query(None, description="Filtrar por invitaciones solicitadas")):
    try:
        print(requested)
        invitations = invitation_service.get_invitations_by_group_id(db, id_group, requested)
        users = invitation_service.get_users_by_invitations(db, invitations)
        if not users:
            return ResponseModel(
                code=1,
                message="NOT FOUND",
                detail="No users found for these invitations",
                dataModel=[]
            )
        
        return ResponseModel(
            code=0,
            message="OK",
            detail="Users retrieved successfully",
            dataModel=users
        )
    except Exception as e:
        return ResponseModel(
            code=1, 
            message="ERROR",
            detail=str(e),
            dataModel=None
        )

@router.get("/invitations/requested/group/{id_group}", response_model=ResponseModel)
async def get_requested_invitations_by_group_id(id_group: int, db: Session = Depends(get_db)):
    try:
        invitations = invitation_service.get_invitations_by_group_id(db, id_group)
        if not invitations:
            return ResponseModel(
                code=1,
                message="NOT FOUND",
                detail="No invitations requested found for this group",
                dataModel=[]
            )
        return ResponseModel(
            code=0,
            message="OK",
            detail="Invitations retrieved successfully",
            dataModel=invitations
        )
    except Exception as e:
        return ResponseModel(
            code=1, 
            message="ERROR",
            detail=str(e),
            dataModel=None
        )




