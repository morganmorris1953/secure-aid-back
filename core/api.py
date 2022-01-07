from ninja import NinjaAPI
from auth_app.api import router as auth_router

api = NinjaAPI()


api.add_router("/auth", auth_router, tags=["Authentication"])
