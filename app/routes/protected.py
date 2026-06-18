# app/routes/protected.py

from fastapi import APIRouter, Depends
from app.dependencies import get_current_user, require_scope

router = APIRouter(
    prefix="/protected",
    tags=["Protected"]
)

@router.get("/profile")
def profile(
    current_user=Depends(get_current_user)
):
    return {
        "message": "OAuth Resource Accessed",
        "email": current_user.email
    }

@router.get("/admin-data")
def admin_data(
    current_user=Depends(
        require_scope("users:write")
    )
):
    return {
        "message": "Admin Resource"
    }