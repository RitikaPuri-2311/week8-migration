from fastapi import APIRouter, Depends

from app.dependencies import get_current_user, require_scope

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/me")
def get_me(
    current_user=Depends(get_current_user)
    
):
    return current_user

@router.get(
    "/admin"
)
def admin_panel(
    permission=Depends(
        require_scope(
            "users:write"
        )
    )
):
    return {
        "message": "Welcome Admin"
    }