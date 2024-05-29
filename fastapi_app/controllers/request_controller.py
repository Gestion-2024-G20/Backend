from typing import Any
from fastapi import APIRouter, Depends
from pyparsing import List
from sqlalchemy.orm import Session
from fastapi_app.get_db import get_db
from fastapi_app.models import Request, ResponseModel, Invitation
from fastapi_app.services import request_service, invitation_service
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/requests")
async def create_request_url(request: Request, db: Session = Depends(get_db)):
    try:
        request = request_service.create_request_url(db, request)
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

@router.post("/requests/join/{userId}")
async def send_request(userId, request: Request, db: Session = Depends(get_db)):
    try:
        res_old_invitation = request_service.get_request_by_user_id_to_group(db, userId, request.id_group)
        if res_old_invitation is not None:
            return ResponseModel(
                code=0,
                message="ERROR",
                detail="You already have a request to join this group",
                dataModel=None
            )
        res_request = request_service.find_valid_request(db, request)
        if res_request is None:
            return ResponseModel(
                code=1,
                message="ERROR",
                detail="Invalid token or group id",
                dataModel=None
            )

        # TODO: Validate date
        try:
            res_invitation = invitation_service.create_invitation(db, Invitation(
                id_invitation=-1,
                id_group=res_request.id_group,
                id_user=userId,
                is_request=True
            ))
        except Exception as e:
            return ResponseModel(
                code=2,
                message="ERROR",
                detail="Failed to create request",
                dataModel=None
            )

        return ResponseModel(
            code=0,
            message="OK",
            detail="Request send successfully",
            dataModel=res_invitation
        )
    except Exception as e:
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )