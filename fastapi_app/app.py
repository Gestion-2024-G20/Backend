from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
import fastapi_app.models as models
from sqlalchemy.orm import Session
from typing import List, Optional


import crud, fastapi_app.schemas as schemas, fastapi_app.models as models
from fastapi_app.models import *
from fastapi_app.schemas import *
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # URL del frontend
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

schemas.Base.metadata.create_all(bind=engine)



@app.post("/expenditures")
def create_expenditure(expenditure: models.ExpenditureBase, db: Session = Depends(get_db)):
    try:
        crud.create_expenditure(db=db, expenditure=expenditure)
    except: 
        return ResponseModel(
            code=1,
            message="ERROR",
            detail="",
            dataModel=None
        )
    else: 
        return ResponseModel(
            code=0,
            message="OK",
            detail="",
            dataModel=expenditure
        )


@app.get("/expenditures/{id_group}", response_model=ResponseModel)
def read_expenditures(
    id_group: int, id_user: Optional[int] = None,
    skip: int = 0, limit: int = 100, 
    db: Session = Depends(get_db)
):
    expenditures = crud.get_expenditures(
        db, id_group, id_user, skip=skip, limit=limit
    )
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



@app.post("/users")
def create_user(user: models.User, db: Session = Depends(get_db)):
    try:
        crud.create_user(db=db, user=user)
    except: 
        return ResponseModel(
            code=1,
            message="ERROR",
            detail="",
            dataModel=None
        )
    else: 
        return ResponseModel(
            code=0,
            message="OK",
            detail="",
            dataModel=user
        )


@app.get("/users", response_model=ResponseModel)
def read_users(
    id_user: Optional[int] = None,
    username: Optional[str] = None,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    users = crud.get_users(
        db, skip, limit, id_user, username
    )
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

@app.get("/user/{username}", response_model=ResponseModel)
def read_users(
    username: str,
    db: Session = Depends(get_db)
):
    user = crud.get_user(
        db, username
    )
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


@app.get("/groups")
def get_groups(
    id_group: Optional[int] = None,
    name: Optional[str] = None,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    # TODO: filter by id_user
    groups = crud.get_groups(
        db, skip, limit, id_group, name
    )
    if len(groups) == 0: 
        return ResponseModel(
            code=1,
            message="NOT FOUND",
            detail="",
            dataModel=None
        )
    print(groups)    
    return ResponseModel(
        code=0,
        message="OK",
        detail="",
        dataModel=groups
    )

@app.post("/groups")
def create_group(group: models.Group, db: Session = Depends(get_db)):
    try:
        crud.create_group(db=db, group=group)
    except: 
        return ResponseModel(
            code=1,
            message="ERROR",
            detail="",
            dataModel=None
        )
    else: 
        return ResponseModel(
            code=0,
            message="OK",
            detail="",
            dataModel=group
        )

@app.get("/hello")
async def read_root():
    return {"message": "Estos son los datos desde el backend"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)