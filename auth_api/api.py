from django.contrib.auth.models import User
from django.http import Http404
from ninja import Router
from oauthlib.common import generate_token
from oauthlib.oauth2 import rfc6749

import requests
from requests.structures import CaseInsensitiveDict


from .va_gov import (
    create_session,
    create_session_with_token,
    get_token_from_callback,
    AUTHORIZATION_URL,
    USERINFO_URL,
)
from . import schemas, jwt, models


router = Router()


@router.get("", response=schemas.URL, url_name="authorization_url")
def get_va_gov_user_authorization_url(request):
    state = generate_token()

    sessions = create_session()
    url, state = sessions.authorization_url(AUTHORIZATION_URL)
    return schemas.URL(url=url)


@router.get(
    "/current_user", response=schemas.UserSchema, url_name="current_user", auth=jwt.AuthBearer()
)
def get_current_user(request):
    user = request.auth
    # print(user.groups.first())
    return schemas.UserSchema.from_orm(request.auth)


@router.get("callback", response=schemas.AuthorizationResponse)
def callback_debugger(request, code: str, state: str):

    try:
        token = get_token_from_callback(code=code)
        token = schemas.VAGovToken(**token)

        url = "https://sandbox-api.va.gov/services/veteran_verification/v1/status"

        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Authorization"] = f"Bearer {token.access_token}"

        response = requests.get(url, headers=headers)
        veteran_status = response.json().get("data").get("attributes")

        session = create_session_with_token(token=token)
        response = session.get(USERINFO_URL)
    except rfc6749.errors.InvalidGrantError as e:
        raise Http404(e.error)

    va_profile = schemas.VAGovProfile(**response.json(), **veteran_status)

    if not va_profile.comfirmed_veteran:
        raise Http404("User not comfirmed veteran.")

    user, created = User.objects.get_or_create(**va_profile.to_military_bridge_profile().dict())

    user.groups.add(models.confirmed_veteran_group)

    assert models.is_confirmed_veteran(user)

    jwt_token = jwt.create_access_token(verified_user=user)

    verified_user = schemas.UserSchema.from_orm(user)

    return schemas.AuthorizationResponse(user=verified_user, token=jwt_token)
