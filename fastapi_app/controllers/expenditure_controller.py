from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import crud
from fastapi_app.get_db import get_db
from fastapi_app.schemas import Expenditure
from fastapi_app.models import ExpenditureBase, ResponseModel

router = APIRouter()


@router.post("/expenditures")
def create_expenditure(expenditure: ExpenditureBase, db: Session = Depends(get_db)):
    try:
        expenditure = crud.create_expenditure(db=db, expenditure=expenditure)
    except Exception as e: 
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=e,
            dataModel=None
        )
    else: 
        return ResponseModel(
            code=0,
            message="OK",
            detail="",
            dataModel=expenditure
        )


@router.get("/expenditures/{id_group}", response_model=ResponseModel)
def read_expenditures(
    id_group: int, id_user: Optional[int] = None,
    skip: int = 0, limit: int = 100, 
    db: Session = Depends(get_db)
):
    try:
        expenditures = crud.get_expenditures(
            db, id_group, id_user, skip=skip, limit=limit
        )
    except Exception as e: 
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )
    else: 
        if len(expenditures) == 0: 
                return ResponseModel(
                    code=1,
                    message="NOT FOUND",
                    detail="",
                    dataModel=None
                )
        print(expenditures)

        return ResponseModel(
                code=0,
                message="OK",
                detail="",
                dataModel=expenditures
            )

