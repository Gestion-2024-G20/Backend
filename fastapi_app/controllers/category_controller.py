from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi_app.services import category_service
from fastapi_app.get_db import get_db
from fastapi_app.models import CategoryBase, CategoryShare, ResponseModel
from sqlalchemy import exc
from fastapi_app.exceptions import BackendException

router = APIRouter()

@router.post("/category", response_model=ResponseModel)
def create_category(category: CategoryBase, db: Session = Depends(get_db)):
    try:
        created_category = category_service.create_category(db=db, category=category)
        return ResponseModel(
            code=0,
            message="OK",
            detail="Category created successfully",
            dataModel=created_category
        )
    except exc.IntegrityError:
        return ResponseModel(
            code=2,
            message="ERROR",
            detail='The names of the categories must be unique inside a group',
            dataModel=None)
    except Exception as e: 
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None)
        
@router.get("/category", response_model=ResponseModel)
def get_categories(
    id_group: Optional[int] = None,
    name: Optional[str] = None,
    id_category: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    try:
        categories = category_service.get_categories(
            db=db, skip=skip, limit=limit, id_group=id_group, name=name, id_category=id_category
        )
        if not categories:
            return ResponseModel(
                code=1,
                message="NOT FOUND",
                detail="No categories found",
                dataModel=None
            )
        return ResponseModel(
            code=0,
            message="OK",
            detail="Categories retrieved successfully",
            dataModel=categories
        )
    except Exception as e: 
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )

@router.delete("/category/{category_id}", response_model=ResponseModel)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    try:
        category = category_service.delete_category(db, category_id)
        return ResponseModel(
            code=0,
            message="OK",
            detail="Category deleted successfully",
            dataModel=category
        )
    except BackendException as e:
        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )
    except Exception as e: 
        return ResponseModel(
            code=1,
            message="ERROR",
            detail='Error deleting category',
            dataModel=None
        )
    
@router.put("/category/{category_id}", response_model=ResponseModel)
def update_category(category_id: int, category: CategoryBase, db: Session = Depends(get_db)):
    try:
        updated_category = category_service.update_category(db, category_id, category)
        if not updated_category:
            return ResponseModel(
                code=1,
                message="NOT FOUND",
                detail="Category not found",
                dataModel=None
            )
        return ResponseModel(
            code=0,
            message="OK",
            detail="Category updated successfully",
            dataModel=updated_category
        )
    except Exception as e:
        print(e)

        return ResponseModel(
            code=1,
            message="ERROR",
            detail=str(e),
            dataModel=None
        )
    
