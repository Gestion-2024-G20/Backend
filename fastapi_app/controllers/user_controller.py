from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import crud
from fastapi_app.get_db import get_db
from fastapi_app.models import User, ResponseModel

router = APIRouter()


@router.post("/users")
def create_user(user: User, db: Session = Depends(get_db)):
    try:
        user = crud.create_user(db=db, user=user)
    except Exception as e: 
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )
    else: 
        return ResponseModel(
            code=0,
            message="OK",
            detail="",
            dataModel=user
        )


@router.get("/users", response_model=ResponseModel)
def read_users(
    id_user: Optional[int] = None,
    username: Optional[str] = None,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    try:
        users = crud.get_users(
            db, skip, limit, id_user, username
        )
    except Exception as e: 
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )
    else: 
        if len(users) == 0: 
            return ResponseModel(
                code=1,
                message="NOT FOUND",
                detail="",
                dataModel=None
            )

        print(users)
        return ResponseModel(
            code=0,
            message="OK",
            detail="",
            dataModel=users
        )

@router.get("/user/{username}", response_model=ResponseModel)
def read_users(
    username: str,
    db: Session = Depends(get_db)
):
    try:
        user = crud.get_user(
            db, username
        )
    except Exception as e: 
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )
    else: 
        if user is None: 
            return ResponseModel(
                code=1,
                message="NOT FOUND",
                detail="",
                dataModel=None
            )
        print(user)
        return ResponseModel(
                code=0,
                message="OK",
                detail="",
                dataModel=user
            )
