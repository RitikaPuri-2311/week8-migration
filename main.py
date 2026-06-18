from fastapi import FastAPI

from app.routes.auth import router as auth_router
from app.routes.users import router as users_router

app = FastAPI(
    title="User Analytics API"
)

app.include_router(auth_router)
app.include_router(users_router)


@app.get("/")
def home():
    return {"message": "API Running"}
