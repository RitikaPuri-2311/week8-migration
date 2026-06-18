from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.jwt_handler import verify_token
from app.database import get_db
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = verify_token(token)

    print(payload)   

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    email = payload.get("sub")

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

def require_scope(scope: str):

    def checker(
        token: str = Depends(oauth2_scheme)
    ):

        payload = verify_token(token)

        scopes = payload.get(
            "scopes",
            []
        )

        if scope not in scopes:
            raise HTTPException(
                status_code=403,
                detail="Permission denied"
            )

    return checker