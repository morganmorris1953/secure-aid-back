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


class CreateUser(Schema):
    id: str
    username: str
    active: bool
    verified: bool


class CreateLinkResponse(Schema):
    token: str
    user: CreateUser
    code: str


def create_passwordless_fusion_client():
    return FusionAuthClient(settings.FUSION_PASSWORDLESS_API_KEY, settings.FUSION_AUTH_BASE_URL)


@router.post("/create", url_name="create_user")
def create_user_link(request, username: str):
    client = create_passwordless_fusion_client()

    user_request = {
        "sendSetPasswordEmail": False,
        "skipVerification": True,
        "user": {"username": username, "password": "password"},
    }  # TODO: generate password

    client_response = client.create_user(user_request)
    if client_response.was_successful():
        user = client_response.success_response
    else:
        return HttpResponseBadRequest(str(client_response.error_response))

    # TODO: create user in db here?

    link_request = {
        "applicationId": settings.FUSION_PASSWORDLESS_APP_ID,
        "loginId": username,
        "state": {
            "client_id": settings.FUSION_PASSWORDLESS_APP_ID,
            "redirect_uri": "https://localhost:8000/callback",
            "response_type": "code",
            "scope": "openid",
            "state": "CSRF123",
        },
    }

    link_response = client.start_passwordless_login(link_request)
    if link_response.was_successful():
        code = link_response.success_response
        print(code)
    else:
        return HttpResponseBadRequest(str(link_response.error_response))

    return CreateLinkResponse(**user, **code)


@router.post("/link_login", response=CreateUser)
def login_with_link(request, code: str):
    client = create_passwordless_fusion_client()
    response = client.passwordless_login({"code": code})

    if response.was_successful():
        return response.success_response.get("user")
    else:
        return HttpResponseBadRequest(str(response.error_response))
