from sqlalchemy.orm import Session
from fastapi_app.exceptions import BackendException
from typing import Optional

from fastapi_app.models import CategoryBase
from fastapi_app.schemas import Category

def get_categories(
    db: Session,
    id_group: int,
    skip: Optional[int],
    limit: Optional[int],
    name: Optional[str],
    id_category: Optional[int]
):
    query = db.query(Category)

    if id_group is not None:
        query = query.filter_by(id_group=id_group)
        
    if name is not None:
        query = query.filter_by(name=name)
    
    if id_category is not None:
        query = query.filter_by(id_category=id_category)

    categories = query.offset(skip).limit(limit).all()

    return categories

def create_category(db: Session, category: CategoryBase):
    print("creating category")
    db_category = Category(
        name=category.name,
        description=category.description,
        id_group=category.id_group
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)

    return db_category

def delete_category(db: Session, category_id: int):
    category = db.query(Category).filter_by(id_category=category_id).first()
    if not category:
        print("Not found")
        raise BackendException("Category not found: Category does not exist")
    db.delete(category)
    db.commit()
    return category
