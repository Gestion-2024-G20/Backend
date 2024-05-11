from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi_app.services import group_service
from fastapi_app.get_db import get_db
from fastapi_app.models import GroupBase, ResponseModel

router = APIRouter()

@router.get("/groups", response_model=ResponseModel)
def get_groups(
    id_group: Optional[int] = None,
    name: Optional[str] = None,
    members_count: Optional[int] = None, 
    time_created: Optional[str] = None, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    try:
        groups = group_service.get_groups(
            db, skip, limit, id_group, name, members_count, time_created
        )
        if not groups:
            return ResponseModel(
                code=1,
                message="NOT FOUND",
                detail="No groups found",
                dataModel=None
            )
        return ResponseModel(
            code=0,
            message="OK",
            detail="Groups retrieved successfully",
            dataModel=groups
        )
    except Exception as e: 
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )

@router.post("/groups", response_model=ResponseModel)
def create_group(group: GroupBase, db: Session = Depends(get_db)):
    try:
        group = group_service.create_group(db=db, group=group)
        return ResponseModel(
            code=0,
            message="OK",
            detail="Group created successfully",
            dataModel=group
        )
    except Exception as e: 
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )

@router.delete("/groups/{group_id}", response_model=ResponseModel)
def delete_group(group_id: int, db: Session = Depends(get_db)):
    try:
        deleted_group = group_service.delete_group(db=db, group_id=group_id)
        if not deleted_group:
            return ResponseModel(
                code=1,
                message="NOT FOUND",
                detail="Group not found",
                dataModel=None
            )
        return ResponseModel(
            code=0,
            message="OK",
            detail="Group deleted successfully",
            dataModel=None
        )
    except Exception as e:
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )

@router.put("/groups/{group_id}", response_model=ResponseModel)
def update_group(group_id: int, group: GroupBase, db: Session = Depends(get_db)):
    try:
        updated_group = group_service.update_group(db=db, group_id=group_id, group=group)
        if not updated_group:
            return ResponseModel(
                code=1,
                message="NOT FOUND",
                detail="Group not found",
                dataModel=None
            )
        return ResponseModel(
            code=0,
            message="OK",
            detail="Group updated successfully",
            dataModel=updated_group
        )
    except Exception as e:
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )
