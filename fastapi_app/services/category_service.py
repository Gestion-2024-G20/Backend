from sqlalchemy.orm import Session

from fastapi_app.models import CategoryBase
from fastapi_app.schemas import Category

def get_categories(
    db: Session,
    skip: int,
    limit: int,
    id_group: int,
    name: str
):
    query = db.query(Category)

    if id_group is not None:
        query = query.filter_by(id_group=id_group)
        
    if name is not None:
        query = query.filter_by(name=name)

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

def delete_category(db: Session, category: CategoryBase):
    db_category = db.query(Category).filter_by(id_category=str(category.id_category), id_group=str(category.id_group)).first()
    if db_category is None:
        print("Not found")
        raise KeyError("Category not found: Category does not exist")
    db.delete(db_category)
    db.commit()
    return db_category
