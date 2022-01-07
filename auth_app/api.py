from ninja import Router, Schema
from pydantic import AnyHttpUrl

from django.http import HttpResponseBadRequest
from django.shortcuts import reverse, get_object_or_404
from django.contrib.auth.models import User
from django.conf import settings

from fusionauth.fusionauth_client import FusionAuthClient


class LoginURL(Schema):
    url: AnyHttpUrl


class UserResponse(Schema):
    id: int
    username: str


router = Router()


def create_fusion_client():
    return FusionAuthClient(settings.FUSION_AUTH_API_KEY, settings.FUSION_AUTH_BASE_URL)


def get_login_url(redirect_uri):
    return f"{settings.FUSION_AUTH_BASE_URL}/oauth2/authorize?client_id={settings.FUSION_AUTH_APP_ID}&redirect_uri={redirect_uri}&response_type=code"


@router.get("/login", url_name="login", response=LoginURL)
def get_login_url_link(request):
    redirect_uri = request.build_absolute_uri(reverse("api-1.0.0:callback"))
    login_url = get_login_url(redirect_uri)
    return LoginURL(url=login_url)


@router.get("/callback", url_name="callback", response=UserResponse)
def callback(request, code):
    redirect_uri = request.build_absolute_uri(reverse("api-1.0.0:callback"))
    client = create_fusion_client()
    response = client.exchange_o_auth_code_for_access_token(
        code, settings.FUSION_AUTH_APP_ID, redirect_uri, settings.FUSION_AUTH_CLIENT_SECRET
    )
    if response.was_successful():
        access_token = response.success_response.get("access_token")
        user_id = response.success_response.get("userId")
        user, created = User.objects.get_or_create(username=user_id)
        return UserResponse.from_orm(user)
    else:
        return HttpResponseBadRequest(str(response.error_response))
