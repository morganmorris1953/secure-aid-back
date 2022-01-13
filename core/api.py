from ninja import NinjaAPI

from auth_api.api import router as auth_router
from auth_api.jwt import AuthBearer
from passwordless_api.api import router as onetime_router

api = NinjaAPI(title="Secure Aid API", version="1.0.0")


api.add_router("/auth", auth_router, tags=["Authentication"])
api.add_router("/onetime", onetime_router, tags=["One Time Token"], auth=AuthBearer())
