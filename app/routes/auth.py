from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies import require_scope
from app.dependencies import require_scope
from app.jwt_handler import create_access_token, create_refresh_token, hash_token
from app.models import RefreshToken
from datetime import datetime

from app.database import get_db
from app.models import User

from app.schemas import (
    UserCreate,
    UserResponse,
    LoginRequest,
    TokenResponse
)

from app.auth import (
    hash_password,
    verify_password
)

from app.jwt_handler import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # ACCESS TOKEN
    access_token = create_access_token(
    {
        "sub": user.email,
        "scopes": [
            "users:read",
            "users:write"
           
        ]
    }
)
    # REFRESH TOKEN
    refresh_token, expires_at = create_refresh_token()

    db_token = RefreshToken(
        user_id=user.id,
        token_hash=hash_token(refresh_token),
        expires_at=expires_at
    )

    db.add(db_token)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh")
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):

    token_hash = hash_token(refresh_token)

    stored_token = db.query(RefreshToken).filter(
        RefreshToken.token_hash == token_hash,
        RefreshToken.is_revoked == False
    ).first()

    if not stored_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if stored_token.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Refresh token expired")

    user = db.query(User).filter(User.id == stored_token.user_id).first()

    new_access_token = create_access_token({"sub": user.email})

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }

@router.post("/logout")
def logout(refresh_token: str, db: Session = Depends(get_db)):

    token_hash = hash_token(refresh_token)

    stored_token = db.query(RefreshToken).filter(
        RefreshToken.token_hash == token_hash
    ).first()

    if not stored_token:
        raise HTTPException(status_code=404, detail="Token not found")

    stored_token.is_revoked = True
    db.commit()

    return {"message": "Logged out successfully"}

