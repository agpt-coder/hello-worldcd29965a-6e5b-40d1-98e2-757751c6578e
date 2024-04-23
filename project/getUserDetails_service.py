from datetime import datetime

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class UserDetailsResponse(BaseModel):
    """
    Provides detailed queried information about the authenticated user after token validation.
    """

    username: str
    role: prisma.enums.Role
    registration_date: datetime


async def getUserDetails(AuthenticationToken: str) -> UserDetailsResponse:
    """
    Retrieves detailed information about the currently authenticated user, such as username, role, and registration date.
    This function assumes the AuthenticationToken is an ID directly linked to the user in the database and was used for simplification.

    Args:
        AuthenticationToken (str): JWT token used to authenticate and identify the user, assumed here to be directly the user's database ID for simplification.

    Returns:
        UserDetailsResponse: Provides detailed queried information about the authenticated user after token validation.

    Example:
        userDetails = getUserDetails('1') # Assuming '1' is a valid user ID
        > UserDetailsResponse(username='user@example.com', role='prisma.models.User', registration_date=datetime(2022, 1, 1))
    """
    user_id = int(AuthenticationToken)
    user = await prisma.models.User.prisma().find_unique(where={"id": user_id})
    if not user:
        raise ValueError("No user found with the provided token")
    response = UserDetailsResponse(
        username=user.email, role=user.role, registration_date=datetime.now()
    )
    return response
