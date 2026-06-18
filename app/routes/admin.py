from fastapi import APIRouter, Depends

from app.permissions import require_permission

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/")
def admin_dashboard(
    current_user=Depends(
        require_permission("users:admin")
    )
):
    return {
        "message": "Welcome Admin",
        "user": current_user.email
    }