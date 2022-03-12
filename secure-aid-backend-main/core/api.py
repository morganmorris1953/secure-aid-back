from ninja import NinjaAPI

from auth_api.api import router as auth_router
from auth_api.jwt import AuthBearer, InvalidToken, VeteranAuthBearer
from passwordless_api.api import router as onetime_router
from user_api.api import router as user_router

api = NinjaAPI(title="Secure Aid API", version="1.0.0")


@api.exception_handler(InvalidToken)
def on_invalid_token(request, exc):
    detail = {"detail": "Could not validate token."}
    return api.create_response(request, detail, status=401)


api.add_router("/auth", auth_router, tags=["Authentication"])
api.add_router("/onetime", onetime_router, tags=["One Time Token"])
# api.add_router("/user", user_router, tags=["User"], auth=VeteranAuthBearer())
api.add_router("/user", user_router, tags=["User"])
