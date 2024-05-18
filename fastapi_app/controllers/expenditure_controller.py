from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi_app.services import expenditure_service
from fastapi_app.get_db import get_db
from fastapi_app.models import ExpenditureBase, ResponseModel

router = APIRouter()

@router.post("/expenditures", response_model=ResponseModel)
def create_expenditure(expenditure: ExpenditureBase, db: Session = Depends(get_db)):
    try:
        created_expenditure = expenditure_service.create_expenditure(db=db, expenditure=expenditure)
        return ResponseModel(
            code=0,
            message="OK",
            detail="Expenditure created successfully",
            dataModel=created_expenditure
        )
    except Exception as e: 
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )


@router.get("/expenditures/{id_group}", response_model=ResponseModel)
def read_expenditures(
    id_group: int, id_user: Optional[int] = None,
    skip: int = 0, limit: int = 100, 
    db: Session = Depends(get_db)
):
    try:
        expenditures = expenditure_service.get_expenditures(
            db, id_group, id_user, skip=skip, limit=limit
        )
        if not expenditures:
            return ResponseModel(
                code=1,
                message="NOT FOUND",
                detail="No expenditures found",
                dataModel=None
            )
        return ResponseModel(
            code=0,
            message="OK",
            detail="Expenditures retrieved successfully",
            dataModel=expenditures
        )
    except Exception as e: 
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )


@router.delete("/expenditures/{expenditure_id}", response_model=ResponseModel)
def delete_expenditure(expenditure_id: int, db: Session = Depends(get_db)):
    try:
        deleted_expenditure = expenditure_service.delete_expenditure(db=db, expenditure_id=expenditure_id)
        if not deleted_expenditure:
            return ResponseModel(
                code=1,
                message="NOT FOUND",
                detail="Expenditure not found",
                dataModel=None
            )
        return ResponseModel(
            code=0,
            message="OK",
            detail="Expenditure deleted successfully",
            dataModel=None
        )
    except Exception as e:
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )


@router.put("/expenditures/{expenditure_id}", response_model=ResponseModel)
def update_expenditure(
    expenditure_id: int, expenditure: ExpenditureBase, db: Session = Depends(get_db)
):
    try:
        updated_expenditure = expenditure_service.update_expenditure(db=db, expenditure_id=expenditure_id, expenditure=expenditure)
        if not updated_expenditure:
            return ResponseModel(
                code=1,
                message="NOT FOUND",
                detail="Expenditure not found",
                dataModel=None
            )
        return ResponseModel(
            code=0,
            message="OK",
            detail="Expenditure updated successfully",
            dataModel=updated_expenditure
        )
    except Exception as e:
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )
