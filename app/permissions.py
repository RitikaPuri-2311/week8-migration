from fastapi import Depends
from fastapi import HTTPException

from app.dependencies import get_current_user


def require_permission(permission: str):

    def checker(
        current_user=Depends(get_current_user)
    ):

        if permission not in current_user.permissions:
            raise HTTPException(
                status_code=403,
                detail="Permission denied"
            )

        return current_user

    return checker