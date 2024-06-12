from typing import Any
from fastapi import APIRouter, Depends
from pyparsing import List
from sqlalchemy.orm import Session
from fastapi_app.get_db import get_db
from fastapi_app.models import Request, ResponseModel
from fastapi_app.services import statistics_service

router = APIRouter()

@router.get("/statistics/{id_group}")
async def get_statistics(id_group: int, db: Session = Depends(get_db)):
    try:
        statistics = statistics_service.get_statistics(db, id_group)
        return ResponseModel(
            code=0,
            message="OK",
            detail="Statistics obtained successfully",
            dataModel=statistics
        )
    except Exception as e:
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )