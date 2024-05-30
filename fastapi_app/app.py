from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import fastapi_app.schemas as schemas
from fastapi_app.models import *
from fastapi_app.database import engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi_app.controllers import category_shares_controller, expenditure_share_controller, group_controller, user_controller, expenditure_controller, group_member_controller, category_controller, invitation_controller, balance_controller, request_controller

app = FastAPI()

app.include_router(expenditure_controller.router)
app.include_router(expenditure_share_controller.router)
app.include_router(group_member_controller.router)
app.include_router(category_shares_controller.router)
app.include_router(group_controller.router)
app.include_router(user_controller.router)
app.include_router(category_controller.router)
app.include_router(invitation_controller.router)
app.include_router(balance_controller.router)
app.include_router(request_controller.router)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # URL del frontend
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

schemas.Base.metadata.create_all(bind=engine)


@app.get("/hello")
async def read_root():
    return {"message": "Estos son los datos desde el backend"}

if __name__ == "__main__":
    uvicorn.run("fastapi_app.app:app", host="0.0.0.0", port=8000, reload=True)
