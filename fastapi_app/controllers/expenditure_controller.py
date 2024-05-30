from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi_app.services import expenditure_service
from fastapi_app.get_db import get_db
from fastapi_app.models import ExpenditureBase, ResponseModel

router = APIRouter()

#Crear un expenditure
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


#Obtener los expenditures de un grupo
@router.get("/expenditures/{id_group}", response_model=ResponseModel)
def read_group_expenditures(
    id_group: int,
    id_user: Optional[int] = None,
    id_category: Optional[int] = None,
    min_date: Optional[str] = None,
    max_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    try:
        expenditures = expenditure_service.get_group_expenditures(
            db, id_group, id_user, id_category, min_date, max_date
        )
        if not expenditures:
            return ResponseModel(
                code=1,
                message="NOT FOUND",
                detail="No expenditures found",
                dataModel=[]
            )
        return ResponseModel(
            code=0,
            message="OK",
            detail="Expenditures retrieved successfully",
            dataModel=expenditures
        )
    except Exception as e: 
        return ResponseModel(
            code=2,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )

# Borrar expenditure
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
            dataModel=deleted_expenditure
        )
    except Exception as e:
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
    )



# modificacion de expenditure
@router.put("/expenditures/{expenditure_id}", response_model=ResponseModel)
def update_expenditure(
    expenditure_id: int, expenditure: ExpenditureBase, db: Session = Depends(get_db)
):
    try:
        updated_expenditure = expenditure_service.update_expenditure(db=db, expenditure_id=expenditure_id, updated_expenditure=expenditure)
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
