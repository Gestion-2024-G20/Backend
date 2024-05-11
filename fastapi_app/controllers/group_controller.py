from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import crud
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
        groups = crud.get_groups(
            db, skip, limit, id_group, name, members_count, time_created
        )
    except Exception as e: 
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )
    else: 
        if len(groups) == 0: 
            return ResponseModel(
                code=1,
                message="NOT FOUND",
                detail="",
                dataModel=None
            )
        print(groups)    
        return ResponseModel(
            code=0,
            message="OK",
            detail="",
            dataModel=groups
        )

@router.post("/groups", response_model=ResponseModel)
def create_group(group: GroupBase, db: Session = Depends(get_db)):
    try:
        group = crud.create_group(db=db, group=group)
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
            dataModel=group
        )
