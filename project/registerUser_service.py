import bcrypt
import prisma
import prisma.models
from pydantic import BaseModel


class UserRegistrationResponse(BaseModel):
    """
    Response returned upon successful user registration, including confirmation message.
    """

    message: str


async def registerUser(
    username: str, password: str, email: str
) -> UserRegistrationResponse:
    """
    This endpoint allows new users to register. It accepts user details like username,
    password, and email, processes them to create a new user account. The password is hashed
    for security, and an initial user role is set. On successful registration, it returns a
    confirmation message.

    Args:
        username (str): Unique identifier for the user account. Must be unique across the system.
        password (str): Password for the user account. Will be hashed before storage for security.
        email (str): Email address associated with the user account. Must be a valid email format and unique.

    Returns:
        UserRegistrationResponse: Response returned upon successful user registration, including confirmation message.
    """
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    user = await prisma.models.User.prisma().create(
        data={
            "username": username,
            "email": email,
            "password": hashed_password.decode("utf-8"),
            "role": "User",
        }
    )
    return UserRegistrationResponse(message="User registered successfully.")
