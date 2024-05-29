from typing import Optional
from fastapi import APIRouter, Depends
from pyparsing import List
from sqlalchemy.orm import Session
from fastapi_app.get_db import get_db
from fastapi_app.models import Request, ResponseModel
from fastapi_app.services import request_service

router = APIRouter()

@router.post("/requests")
async def create_request(request: Request, db: Session = Depends(get_db)):
    try:
        request = request_service.create_request(db, request)
        return ResponseModel(
            code=0,
            message="OK",
            detail="Url created successfully",
            dataModel=request
        )
    except Exception as e:
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )
