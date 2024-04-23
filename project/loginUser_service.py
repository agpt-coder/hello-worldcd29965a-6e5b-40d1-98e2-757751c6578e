from datetime import datetime, timedelta
from typing import Optional

import bcrypt
import jwt
import prisma
import prisma.models
from pydantic import BaseModel


class LoginResponse(BaseModel):
    """
    This model encapsulates the response from the login attempt, which could either be a JWT token on successful authentication or an error message on failure.
    """

    token: str
    error: Optional[str] = None


async def loginUser(username: str, password: str) -> LoginResponse:
    """
    This endpoint authenticates a user by checking username and password against stored records. If credentials are valid, it generates and returns an authentication token (JWT) used for subsequent requests. On failure, it returns an error message.

    Args:
        username (str): The username of the user trying to log in.
        password (str): The password of the user, which needs to be verified against the stored record for authentication.

    Returns:
        LoginResponse: This model encapsulates the response from the login attempt, which could either be a JWT token on successful authentication or an error message on failure.
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": username})
    if user and bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        expiration_time = datetime.utcnow() + timedelta(days=2)
        payload = {
            "user_id": user.id,
            "email": user.email,
            "role": user.role.name,
            "exp": expiration_time,
        }
        token = jwt.encode(payload, "your_jwt_secret_here", algorithm="HS256")
        return LoginResponse(token=token)
    return LoginResponse(token="", error="Invalid login credentials.")
