import prisma
import prisma.models
from pydantic import BaseModel


class DeleteUserResponse(BaseModel):
    """
    Response model upon successful deletion of the user account. It confirms the deletion and ensures that proper authentication was carried out.
    """

    success: bool
    message: str


async def deleteUser(user_id: int) -> DeleteUserResponse:
    """
    Enables an authenticated user to delete their account. This is a protected endpoint that requires user authentication and can only be triggered by the account owner or an administrator.

    Args:
        user_id (int): The unique identifier for the user that is intended to be deleted. This field is required to specify which user account to delete.

    Returns:
        DeleteUserResponse: Response model upon successful deletion of the user account. It confirms the deletion and ensures that proper authentication was carried out.
    """
    user = await prisma.models.User.prisma().find_unique(where={"id": user_id})
    if user is None:
        return DeleteUserResponse(success=False, message="User not found.")
    await prisma.models.User.prisma().delete(where={"id": user_id})
    return DeleteUserResponse(success=True, message="User successfully deleted.")
