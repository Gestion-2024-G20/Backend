from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi_app.services import user_service
from fastapi_app.get_db import get_db
from fastapi_app.models import User, ResponseModel
from fastapi_app.services import group_service
from fastapi_app.services import group_member_service
from fastapi_app import models


router = APIRouter()


#Guardar un usuario
@router.post("/users")
def create_user(user: User, db: Session = Depends(get_db)):
    try:
        user = user_service.create_user(db=db, user=user)
        return ResponseModel(
            code=0,
            message="OK",
            detail="User created successfully",
            dataModel=user
        )
    except Exception as e: 
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )


#Obtener todos los usuarios
@router.get("/users", response_model=ResponseModel)
def read_users(
    id_user: Optional[int] = None,
    username: Optional[str] = None,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    try:
        users = user_service.get_users(
            db, skip, limit, id_user, username
        )
        if not users:
            return ResponseModel(
                code=1,
                message="NOT FOUND",
                detail="No users found",
                dataModel=None
            )
        return ResponseModel(
            code=0,
            message="OK",
            detail="Users retrieved successfully",
            dataModel=users
        )
    except Exception as e: 
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )


#Obtener usuario por id
@router.get("/user/{id_user}", response_model=ResponseModel)
def read_user(
    id_user: int,
    db: Session = Depends(get_db)
):
    try:
        user = user_service.get_user(
            db, id_user
        )
        if not user:
            return ResponseModel(
                code=1,
                message="NOT FOUND",
                detail="User not found",
                dataModel=None
            )
        return ResponseModel(
            code=0,
            message="OK",
            detail="User retrieved successfully",
            dataModel=user
        )
    except Exception as e: 
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )


#Borrar un usuario
@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    try:
        deleted_user = user_service.delete_user(db=db, user_id=user_id)
        if not deleted_user:
            return ResponseModel(
                code=1,
                message="NOT FOUND",
                detail="User not found",
                dataModel=None
            )
        return ResponseModel(
            code=0,
            message="OK",
            detail="User deleted successfully",
            dataModel=None
        )
    except Exception as e:
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )


#Actualizar un usuario
@router.put("/users/{user_id}")
def update_user(
    user_id: int,
    user: User,
    db: Session = Depends(get_db)
):
    try:
        updated_user = user_service.update_user(db=db, user_id=user_id, user=user)
        if not updated_user:
            return ResponseModel(
                code=1,
                message="NOT FOUND",
                detail="User not found",
                dataModel=None
            )
        return ResponseModel(
            code=0,
            message="OK",
            detail="User updated successfully",
            dataModel=updated_user
        )
    except Exception as e:
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )