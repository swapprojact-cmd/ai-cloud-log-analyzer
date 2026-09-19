from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self) -> None:
        self.secret = os.getenv("AUTH_JWT_SECRET", "change-me-in-production")

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, password: str, password_hash: str) -> bool:
        return pwd_context.verify(password, password_hash)

    def create_token(self, user_id: str) -> str:
        payload = {"sub": user_id, "exp": datetime.now(timezone.utc) + timedelta(hours=24)}
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def decode_token(self, token: str) -> dict:
        return jwt.decode(token, self.secret, algorithms=["HS256"])
