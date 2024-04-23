from typing import Optional

import bcrypt
import jwt
import prisma
import prisma.enums
import prisma.models
from jwt import ExpiredSignatureError, PyJWTError
from pydantic import BaseModel


class User(BaseModel):
    """
    A representation of the updated user profile including critical information like email and role.
    """

    email: str
    role: prisma.enums.Role


class UserProfileUpdateResponse(BaseModel):
    """
    The response after a user profile update operation, indicating success or failure and any relevant user data.
    """

    success: bool
    message: str
    updated_user: Optional[User] = None


SECRET_KEY = "YourSecretKeyHere"

ALGORITHM = "HS256"


async def updateUserDetails(
    email: str, password: str, auth_token: str
) -> UserProfileUpdateResponse:
    """
    Allows authenticated users to update their profile information like email and password. Users need to be authenticated and can only update their own information. It requires passing the new details and the authentication token.

    Args:
    email (str): The new email address to update the user's profile.
    password (str): The new password for the user. It should be securely hashed and validated before use.
    auth_token (str): The JWT token used for authenticating the user's request, ensuring they are updating their own profile only.

    Returns:
    UserProfileUpdateResponse: The response after a user profile update operation, indicating success or failure and any relevant user data.
    """
    try:
        data = jwt.decode(auth_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = data["user_id"]
        user = await prisma.models.User.prisma().find_unique(where={"id": user_id})
        if user is None:
            return UserProfileUpdateResponse(success=False, message="User not found.")
        if user.email != email:
            existing_user = await prisma.models.User.prisma().find_unique(
                where={"email": email}
            )
            if existing_user:
                return UserProfileUpdateResponse(
                    success=False, message="Email already in use."
                )
            user = await prisma.models.User.prisma().update(
                where={"id": user_id}, data={"email": email}
            )
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = await prisma.models.User.prisma().update(
            where={"id": user_id}, data={"password": hashed_password.decode()}
        )
        updated_user = User(email=user.email, role=user.role.name)
        return UserProfileUpdateResponse(
            success=True,
            message="User profile updated successfully.",
            updated_user=updated_user,
        )
    except ExpiredSignatureError:
        return UserProfileUpdateResponse(
            success=False, message="Authentication failed due to expired token."
        )
    except PyJWTError as e:
        return UserProfileUpdateResponse(
            success=False, message=f"Authentication failed: {str(e)}"
        )
    except Exception as e:
        return UserProfileUpdateResponse(
            success=False, message=f"Update failed: {str(e)}"
        )
