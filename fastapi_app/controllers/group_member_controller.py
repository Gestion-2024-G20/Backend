from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import crud
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
        group_members = crud.get_group_members(
            db, skip, limit, id_group, id_user, is_admin
        )
    except Exception as e: 
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )
    else: 
        if len(group_members) == 0: 
            return ResponseModel(
                code=1,
                message="NOT FOUND",
                detail="",
                dataModel=None
            )
        print(group_members)    
        return ResponseModel(
            code=0,
            message="OK",
            detail="",
            dataModel=group_members
        )

@router.post("/groupMember", response_model=ResponseModel)
def create_group_member(group_member: GroupMember, db: Session = Depends(get_db)):
    try:
        group_member =crud.create_group_member(db, group_member)
    except Exception as e: 
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )
    else: 
        return ResponseModel(
            code=0,
            message="OK",
            detail="",
            dataModel=group_member
        )
 