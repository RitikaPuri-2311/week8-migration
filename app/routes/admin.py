from fastapi import APIRouter, Depends
from pytest import Session

from app.database import get_db
from app.models import Permission, Role, RolePermission, UserRole
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


@router.post("/roles")
def create_role(
    name: str,
    db: Session = Depends(get_db)
):
    role = Role(name=name)

    db.add(role)
    db.commit()

    return role

@router.post("/permissions")
def create_permission(
    name: str,
    db: Session = Depends(get_db)
):
    permission = Permission(
        name=name
    )

    db.add(permission)
    db.commit()

    return permission

@router.post("/assign-role")
def assign_role(
    user_id: int,
    role_id: int,
    db: Session = Depends(get_db)
):
    user_role = UserRole(
        user_id=user_id,
        role_id=role_id
    )

    db.add(user_role)
    db.commit()

    return {
        "message": "Role assigned"
    }

@router.post("/assign-permission")
def assign_permission(
    role_id: int,
    permission_id: int,
    db: Session = Depends(get_db)
):
    rp = RolePermission(
        role_id=role_id,
        permission_id=permission_id
    )

    db.add(rp)
    db.commit()

    return {
        "message": "Permission assigned"
    }