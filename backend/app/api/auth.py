from fastapi import APIRouter

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register")
def register(payload: dict) -> dict:
    return {"message": "Registration endpoint ready", "email": payload.get("email")}


@router.post("/login")
def login(payload: dict) -> dict:
    return {"message": "Login endpoint ready", "email": payload.get("email")}


@router.get("/me")
def me() -> dict:
    return {"authenticated": False}
