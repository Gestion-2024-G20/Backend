from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi_app.services import category_share_service
from fastapi_app.get_db import get_db
from fastapi_app.models import CategoryShare, ResponseModel

router = APIRouter()

@router.get("/categoryShares", response_model=ResponseModel)
def get_category_shares(
    id_cs: Optional[int] = None,
    id_category: Optional[int] = None,
    id_user: Optional[int] = None,
    share_percentage: Optional[int] = None, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    try:
        category_shares = category_share_service.get_category_shares(
            db, skip, limit, id_cs, id_category, id_user, share_percentage
        )
        if not category_shares:
            return ResponseModel(
                code=1,
                message="NOT FOUND",
                detail="No category shares found",
                dataModel=None
            )
        return ResponseModel(
            code=0,
            message="OK",
            detail="Category shares retrieved successfully",
            dataModel=category_shares
        )
    except Exception as e: 
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )

@router.get("/categoryShares/id_group={id_group}", response_model=ResponseModel)
def get_group_category_shares(id_group: int, db: Session = Depends(get_db)):

    try:
        category_shares = category_share_service.get_group_category_shares(
            db, id_group
        )
        if not category_shares:
            return ResponseModel(
                code=1,
                message="NOT FOUND",
                detail="No category shares found",
                dataModel=None
            )
        return ResponseModel(
            code=0,
            message="OK",
            detail="Category shares retrieved successfully",
            dataModel=category_shares
        )
    except Exception as e: 
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )
@router.post("/categoryShares", response_model=ResponseModel)
def create_category_share(category_share: CategoryShare, db: Session = Depends(get_db)):
    try:
        created_category_share = category_share_service.create_category_share(db=db, category_share=category_share)
        return ResponseModel(
            code=0,
            message="OK",
            detail="Category share created successfully",
            dataModel=created_category_share
        )
    except Exception as e: 
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )

@router.delete("/categoryShares/{category_share_id}", response_model=ResponseModel)
def delete_category_share(category_share_id: int, db: Session = Depends(get_db)):
    try:
        deleted_category_share = category_share_service.delete_category_share(db=db, category_share_id=category_share_id)
        if not deleted_category_share:
            return ResponseModel(
                code=1,
                message="NOT FOUND",
                detail="Category share not found",
                dataModel=None
            )
        return ResponseModel(
            code=0,
            message="OK",
            detail="Category share deleted successfully",
            dataModel=None
        )
    except Exception as e:
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )

@router.delete("/categoryCategoryShares/{category_id}", response_model=ResponseModel)
def delete_category_category_shares(category_id: int, db: Session = Depends(get_db)):
    try:
        deleted_category_shares = category_share_service.delete_category_category_shares(db=db, category_id=category_id)
        if not deleted_category_shares or len(deleted_category_shares) == 0:
            return ResponseModel(
                code=0,
                message="NOT FOUND",
                detail="Category shares not found",
                dataModel=None
            )
        return ResponseModel(
            code=0,
            message="OK",
            detail=len(deleted_category_shares) + " Category shares deleted successfully",
            dataModel=None
        )
    except Exception as e:
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )

@router.put("/categoryShares/{category_share_id}", response_model=ResponseModel)
def update_category_share(
    category_share_id: int, category_share: CategoryShare, db: Session = Depends(get_db)
):
    try:
        updated_category_share = category_share_service.update_category_share(db=db, category_share_id=category_share_id, category_share=category_share)
        if not updated_category_share:
            return ResponseModel(
                code=1,
                message="NOT FOUND",
                detail="Category share not found",
                dataModel=None
            )
        return ResponseModel(
            code=0,
            message="OK",
            detail="Category share updated successfully",
            dataModel=updated_category_share
        )
    except Exception as e:
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )
