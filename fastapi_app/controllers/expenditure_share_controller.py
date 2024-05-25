from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi_app.services import expenditure_share_service
from fastapi_app.get_db import get_db
from fastapi_app.models import ExpenditureShare, ResponseModel

router = APIRouter()

@router.post("/expenditure-shares", response_model=ResponseModel)
def create_expenditure_share(expenditure_share: ExpenditureShare, db: Session = Depends(get_db)):
    try:
        created_expenditure_share = expenditure_share_service.create_expenditure_share(db=db, expenditure_share=expenditure_share)
        return ResponseModel(
            code=0,
            message="OK",
            detail="Expenditure Share created successfully",
            dataModel=created_expenditure_share
        )
    except Exception as e: 
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )

@router.get("/expenditure-shares", response_model=ResponseModel)
def read_expenditure_shares(
    id_expenditure: Optional[int] = None, id_user: Optional[int] = None,
    skip: int = 0, limit: int = 100, 
    db: Session = Depends(get_db)
):
    try:
        expenditure_shares = expenditure_share_service.get_expenditure_shares(
            db, id_expenditure, id_user, skip=skip, limit=limit
        )
        if not expenditure_shares:
            return ResponseModel(
                code=1,
                message="NOT FOUND",
                detail="No expenditure shares found",
                dataModel=None
            )
        return ResponseModel(
            code=0,
            message="OK",
            detail="Expenditure Shares retrieved successfully",
            dataModel=expenditure_shares
        )
    except Exception as e: 
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )


@router.put("/expenditure-shares/{expenditure_share_id}", response_model=ResponseModel)
def update_expenditure_share(
    expenditure_share_id: int, expenditure_share: ExpenditureShare, db: Session = Depends(get_db)
):
    try:
        updated_expenditure_share = expenditure_share_service.update_expenditure_share(db=db, expenditure_share_id=expenditure_share_id, expenditure_share=expenditure_share)
        if not updated_expenditure_share:
            return ResponseModel(
                code=1,
                message="NOT FOUND",
                detail="Expenditure Share not found",
                dataModel=None
            )
        return ResponseModel(
            code=0,
            message="OK",
            detail="Expenditure Share updated successfully",
            dataModel=updated_expenditure_share
        )
    except Exception as e:
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )
    

@router.delete("/expenditure-shares/{expenditure_share_id}", response_model=ResponseModel)
def delete_expenditure_share(expenditure_share_id: int, db: Session = Depends(get_db)):
    try:
        deleted_expenditure_share = expenditure_share_service.delete_expenditure_share(db=db, expenditure_share_id=expenditure_share_id)
        if not deleted_expenditure_share:
            return ResponseModel(
                code=1,
                message="NOT FOUND",
                detail="Expenditure Share not found",
                dataModel=None
            )
        return ResponseModel(
            code=0,
            message="OK",
            detail="Expenditure Share deleted successfully",
            dataModel=None
        )
    except Exception as e:
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )   
    


@router.delete("/expenditureSharesByExpenditureId/{expenditure_id}", response_model=ResponseModel)
def delete_expenditure_share(expenditure_id: int, db: Session = Depends(get_db)):
    try:
        deleted_expenditure_share = expenditure_share_service.delete_expenditure_share_by_expenditure_id(db=db, expenditure_id=expenditure_id)
        if not deleted_expenditure_share:
            return ResponseModel(
                code=1,
                message="NOT FOUND",
                detail="Expenditure Share not found",
                dataModel=None
            )
        return ResponseModel(
            code=0,
            message="OK",
            detail="Expenditure Shares deleted successfully",
            dataModel=deleted_expenditure_share
        )
    except Exception as e:
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )   
