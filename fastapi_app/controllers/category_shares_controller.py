from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import crud
from fastapi_app.get_db import get_db
from fastapi_app.models import CategoryShare, ResponseModel

router = APIRouter()

@router.get("/categoryShares", response_model=ResponseModel)
def get_category_shares(
    id_group: Optional[int] = None,
    id_user: Optional[int] = None,
    category_name: Optional[str] = None, 
    share_percentage: Optional[int] = None, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    try:
        category_shares = crud.get_category_shares(
            db, skip, limit, id_group, id_user, category_name, share_percentage
        )
    except Exception as e: 
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )
    else: 
        if len(category_shares) == 0: 
            return ResponseModel(
                code=1,
                message="NOT FOUND",
                detail="",
                dataModel=None
            )
        print(category_shares)    
        return ResponseModel(
            code=0,
            message="OK",
            detail="",
            dataModel=category_shares
        )

@router.post("/categoryShares", response_model=ResponseModel)
def create_category_share(category_share: CategoryShare, db: Session = Depends(get_db)):
    try:
        category_share = crud.create_category_share(db, category_share)
    except Exception as e: 
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(type(Exception)) + str(e),
            dataModel=None
        )
    else: 
        return ResponseModel(
            code=0,
            message="OK",
            detail="",
            dataModel=category_share
        )
