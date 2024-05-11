from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi_app.services import group_member_service
from fastapi_app.get_db import get_db
from fastapi_app.models import GroupMember, ResponseModel

router = APIRouter()


@router.get("/groupMembers", response_model=ResponseModel)
def get_group_members(
    id_group: Optional[int] = None,
    id_user: Optional[int] = None,
    is_admin: Optional[bool] = None, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    try:
        group_members = group_member_service.get_group_members(
            db, skip, limit, id_group, id_user, is_admin
        )
        if not group_members:
            return ResponseModel(
                code=1,
                message="NOT FOUND",
                detail="No group members found",
                dataModel=None
            )
        return ResponseModel(
            code=0,
            message="OK",
            detail="Group members retrieved successfully",
            dataModel=group_members
        )
    except Exception as e: 
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )

@router.post("/groupMember", response_model=ResponseModel)
def create_group_member(group_member: GroupMember, db: Session = Depends(get_db)):
    try:
        created_group_member = group_member_service.create_group_member(db=db, group_member=group_member)
        return ResponseModel(
            code=0,
            message="OK",
            detail="Group member created successfully",
            dataModel=created_group_member
        )
    except Exception as e: 
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )

@router.delete("/groupMembers/{group_member_id}", response_model=ResponseModel)
def delete_group_member(group_member_id: int, db: Session = Depends(get_db)):
    try:
        deleted_group_member = group_member_service.delete_group_member(db=db, group_member_id=group_member_id)
        if not deleted_group_member:
            return ResponseModel(
                code=1,
                message="NOT FOUND",
                detail="Group member not found",
                dataModel=None
            )
        return ResponseModel(
            code=0,
            message="OK",
            detail="Group member deleted successfully",
            dataModel=None
        )
    except Exception as e:
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )
