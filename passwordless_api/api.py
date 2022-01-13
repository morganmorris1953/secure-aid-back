from ninja import Router, Schema
from django.urls import reverse
from django.contrib.auth.models import User

from request_token.models import RequestToken
from request_token.utils import decode
from request_token.commands import log_token_use

from django.http import Http404
from auth_api import schemas as auth_schemas, jwt

import hashlib

from typing import Optional
from pydantic import SecretStr

from . import models

router = Router()


class AccountInformation(Schema):
    username: str
    first_name: str
    last_name: str
    email: Optional[str]


def get_password_hash(password: SecretStr):
    plain_text = password.get_secret_value().encode()
    return hashlib.sha256(plain_text).hexdigest()


# TODO: Make sure only confirmed vets can create link.
@router.post("/create_link")
def create_link(request, account_information: AccountInformation, password: SecretStr):
    hashed_password = get_password_hash(password)
    token = RequestToken.objects.create_token(
        scope=hashed_password,
        login_mode=RequestToken.LOGIN_MODE_NONE,
        data=account_information.dict(),
    )
    return request.build_absolute_uri(reverse("api-1.0.0:use_token") + "?token=" + token.jwt())


@router.get("/check", url_name="check_link", response=AccountInformation)
def check_link(request, token: str):
    decoded_token = decode(token)
    token_id = decoded_token.get("jti")
    request_token = RequestToken.objects.get(id=token_id)
    return request_token.data


def use_token(request_token: RequestToken, request):
    request_token.validate_max_uses()
    request_token.authenticate(request)
    log_token_use(request_token, request, 200)


@router.get("/use_token", url_name="use_token")
def use_link(request, token: str, password: SecretStr):
    decoded_token = decode(token)
    token_id = decoded_token.get("jti")
    request_token = RequestToken.objects.get(id=token_id)

    use_token(request_token, request)
    hashed_password = get_password_hash(password)
    if hashed_password != request_token.scope:
        raise Http404("Unauthorized")

    user, created_user = User.objects.get_or_create(**request_token.data)
    user.groups.add(models.approved_recipient)

    if not models.is_approved_recipient(user):
        raise Http404("Unauthorized")

    verified_user = auth_schemas.UserSchema.from_orm(user)
    jwt_token = jwt.create_access_token(verified_user=verified_user)

    return auth_schemas.AuthorizationResponse(user=verified_user, jwt=jwt_token)
