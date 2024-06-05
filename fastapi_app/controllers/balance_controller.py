from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi_app.services import balance_service
from fastapi_app.get_db import get_db
from fastapi_app.models import ResponseModel

router = APIRouter()


@router.get("/balance", response_model=ResponseModel)
def get_balance(
    id_group: int,
    id_user: int,
    db: Session = Depends(get_db)
):
    try:
        balance = balance_service.get_balance(
            db, id_group, id_user,
        )
        if not balance:
            return ResponseModel(
                code=1,
                message="NOT FOUND",
                detail="No balance found",
                dataModel=None
            )
        return ResponseModel(
            code=0,
            message="OK",
            detail="Balance retrieved successfully",
            dataModel=balance
        )
    except Exception as e: 
        return ResponseModel(
            code=2,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )


@router.get("/balance/is_null", response_model=ResponseModel)
def get_balance(
    id_group: int,
    db: Session = Depends(get_db)
):
    try:
        is_null = balance_service.is_null(
            db, id_group
        )
        return ResponseModel(
            code=0,
            message="OK",
            detail="Balance retrieved successfully",
            dataModel=is_null
        )
    except Exception as e: 
        return ResponseModel(
            code=2,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )