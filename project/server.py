import logging
from contextlib import asynccontextmanager

import project.deleteUser_service
import project.executeHelloWorld_service
import project.getHelloWorld_service
import project.getUserDetails_service
import project.loginUser_service
import project.registerUser_service
import project.updateUserDetails_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="hello-world",
    lifespan=lifespan,
    description="create a single hello world app",
)


@app.delete(
    "/user/delete", response_model=project.deleteUser_service.DeleteUserResponse
)
async def api_delete_deleteUser(
    user_id: int,
) -> project.deleteUser_service.DeleteUserResponse | Response:
    """
    Enables an authenticated user to delete their account. This is a protected endpoint that requires user authentication and can only be triggered by the account owner or an administrator.
    """
    try:
        res = await project.deleteUser_service.deleteUser(user_id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/register", response_model=project.registerUser_service.UserRegistrationResponse
)
async def api_post_registerUser(
    username: str, password: str, email: str
) -> project.registerUser_service.UserRegistrationResponse | Response:
    """
    This endpoint allows new users to register. It accepts user details like username, password, and email, processes them to create a new user account. The password is hashed for security, and an initial user role is set. On successful registration, it returns a confirmation message.
    """
    try:
        res = await project.registerUser_service.registerUser(username, password, email)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/login", response_model=project.loginUser_service.LoginResponse)
async def api_post_loginUser(
    username: str, password: str
) -> project.loginUser_service.LoginResponse | Response:
    """
    This endpoint authenticates a user by checking username and password against stored records. If credentials are valid, it generates and returns an authentication token (JWT) used for subsequent requests. On failure, it returns an error message.
    """
    try:
        res = await project.loginUser_service.loginUser(username, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/hello-world", response_model=project.getHelloWorld_service.HelloWorldResponse
)
async def api_get_getHelloWorld(
    user_id: int,
) -> project.getHelloWorld_service.HelloWorldResponse | Response:
    """
    This route serves the classic 'Hello World' message. Upon a GET request, it checks the user's authentication status through the User Management Module. If authenticated, it returns a 'Hello World' message. Unauthenticated requests are denied access, ensuring that the endpoint is secure and respecting the application’s role-based access control.
    """
    try:
        res = await project.getHelloWorld_service.getHelloWorld(user_id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/cli/hello-world",
    response_model=project.executeHelloWorld_service.HelloWorldCommandResponse,
)
async def api_post_executeHelloWorld(
    user_id: int, token: str, command: str
) -> project.executeHelloWorld_service.HelloWorldCommandResponse | Response:
    """
    Accepts and processes the command to output 'Hello World' message. This route first authenticates the user using the User Management Module. If authenticated and authorized (as an Administrator or User), it then executes and returns a 'Hello World' response. If authentication or authorization fails, it should return an appropriate error message explaining the issue.
    """
    try:
        res = await project.executeHelloWorld_service.executeHelloWorld(
            user_id, token, command
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/user/update",
    response_model=project.updateUserDetails_service.UserProfileUpdateResponse,
)
async def api_put_updateUserDetails(
    email: str, password: str, auth_token: str
) -> project.updateUserDetails_service.UserProfileUpdateResponse | Response:
    """
    Allows authenticated users to update their profile information like email and password. Users need to be authenticated and can only update their own information. It requires passing the new details and the authentication token.
    """
    try:
        res = await project.updateUserDetails_service.updateUserDetails(
            email, password, auth_token
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/user/details", response_model=project.getUserDetails_service.UserDetailsResponse
)
async def api_get_getUserDetails(
    AuthenticationToken: str,
) -> project.getUserDetails_service.UserDetailsResponse | Response:
    """
    Retrieves detailed information about the currently authenticated user, such as username, role, and registration date. This endpoint requires a valid authentication token provided in the request header.
    """
    try:
        res = await project.getUserDetails_service.getUserDetails(AuthenticationToken)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
