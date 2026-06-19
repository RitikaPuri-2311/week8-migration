from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

import os
from dotenv import load_dotenv

from app.routes.auth import router as auth_router
from app.routes.users import router as users_router
from app.routes.admin import router as admin_router
from app.routes.protected import router as protected_router
from app.routes.google_auth import ( router as google_router)
from app.routes.admin import router as admin_router

load_dotenv()


app = FastAPI(
    title="User Analytics API"
)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET")
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(admin_router)
app.include_router(protected_router)
app.include_router(google_router)
app.include_router(admin_router)



@app.get("/")
def home():
    return {"message": "API Running"}
