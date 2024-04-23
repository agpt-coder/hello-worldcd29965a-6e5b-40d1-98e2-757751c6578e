import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class HelloWorldResponse(BaseModel):
    """
    Response model for /hello-world endpoint. Delivers a simple 'Hello World' message to authenticated users or a denial message to unauthenticated requests.
    """

    message: str


async def getHelloWorld(user_id: int) -> HelloWorldResponse:
    """
    This route serves the classic 'Hello World' message. Upon a GET request, it checks the user's authentication status through the User Management Module. If authenticated, it returns a 'Hello World' message. Unauthenticated requests are denied access, ensuring that the endpoint is secure and respecting the application’s role-based access control.

    Args:
        user_id (int): The user's ID used for authentication and role verification.

    Returns:
        HelloWorldResponse: Response model for /hello-world endpoint. Delivers a simple 'Hello World' message to authenticated users or a denial message to unauthenticated requests.
    """
    user = await prisma.models.User.prisma().find_unique(where={"id": user_id})
    if user is not None and user.role == prisma.enums.Role.User:
        interaction_response = await prisma.models.Interaction.prisma().create(
            data={
                "userId": user_id,
                "type": prisma.enums.InteractionType.API,
                "content": "Hello World",
            }
        )
        message = interaction_response.content
    else:
        message = "Access denied"
    return HelloWorldResponse(message=message)
