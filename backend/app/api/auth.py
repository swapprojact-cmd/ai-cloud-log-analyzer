from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field

from app.core.supabase import get_anon_client, get_service_client
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


class AuthRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


@router.post("/register")
def register(payload: AuthRequest):
    try:
        result = get_anon_client().auth.sign_up({"email": payload.email, "password": payload.password})
        if not result.user:
            raise HTTPException(status_code=400, detail="Registration failed")
        try:
            get_service_client().table("users").upsert({"id": str(result.user.id), "email": payload.email}).execute()
        except Exception:
            pass
        return {"user": {"id": str(result.user.id), "email": result.user.email}, "session": result.session}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/login")
def login(payload: AuthRequest):
    try:
        result = get_anon_client().auth.sign_in_with_password({"email": payload.email, "password": payload.password})
        if not result.user or not result.session:
            raise HTTPException(status_code=401, detail="Login failed or email confirmation is required")
        return {"user": {"id": str(result.user.id), "email": result.user.email}, "access_token": result.session.access_token, "refresh_token": result.session.refresh_token}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=401, detail="Invalid email or password") from exc


@router.get("/me")
def me(user: dict = Depends(get_current_user)):
    return {"user": user}
