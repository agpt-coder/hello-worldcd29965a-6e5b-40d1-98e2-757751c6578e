import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class HelloWorldCommandResponse(BaseModel):
    """
    The response model for the 'Hello World' command, providing either a success message or an error.
    """

    message: str


async def executeHelloWorld(
    user_id: int, token: str, command: str
) -> HelloWorldCommandResponse:
    """
    Accepts and processes the command to output 'Hello World' message. This route first authenticates the user using the User Management Module. If authenticated and authorized
    (as an Administrator or User), it then executes and returns a 'Hello World' response. If authentication or authorization fails, it should return an appropriate error message explaining the issue.

    Args:
    user_id (int): The user ID used for authenticating the user.
    token (str): The authentication token provided by the user for session verification.
    command (str): The CLI command string, expected to be 'hello-world'.

    Returns:
    HelloWorldCommandResponse: The response model for the 'Hello World' command, providing either a success message or an error.
    """
    user = await prisma.models.User.prisma().find_unique(
        where={"id": user_id, "AND": {"token": token}}
    )
    if not user:
        return HelloWorldCommandResponse(
            message="Authentication failed. User does not exist or token is invalid."
        )
    if command != "hello-world":
        return HelloWorldCommandResponse(
            message="Invalid command. Expected 'hello-world'."
        )
    if user.role in [prisma.enums.Role.User, prisma.enums.Role.Administrator]:
        interaction = await prisma.models.Interaction.prisma().create(
            {
                "userId": user_id,
                "type": prisma.enums.InteractionType.CLI,
                "content": "Hello World",
            }
        )
        return HelloWorldCommandResponse(message="Hello World")
    else:
        return HelloWorldCommandResponse(
            message="Authorization failed. User is not permitted to execute this command."
        )
