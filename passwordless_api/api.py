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
from pydantic import SecretStr, HttpUrl, AnyHttpUrl

from user_api import models as user_models


router = Router()


class AccountInformation(Schema):
    username: str
    first_name: str
    last_name: str
    email: str
    sponsor_id: Optional[int]


class Message(Schema):
    message: str


class URL(Schema):
    url: AnyHttpUrl


def get_password_hash(password: SecretStr):
    plain_text = password.get_secret_value().encode()
    return hashlib.sha256(plain_text).hexdigest()


# TODO: Make sure only confirmed vets can create link.
@router.post("/create_link", auth=jwt.VeteranAuthBearer(), response={200: URL, 400: Message})
def create_link(request, account_information: AccountInformation, link_password: SecretStr):
    user_collision = User.objects.filter(username=account_information.username).exists()
    if user_collision:
        return 400, Message(message="Choose a different username.")

    hashed_password = get_password_hash(link_password)

    account_information.sponsor_id = request.auth.id

    token = RequestToken.objects.create_token(
        scope=hashed_password,
        login_mode=RequestToken.LOGIN_MODE_NONE,
        data=account_information.dict(),
    )
    origin = request.META.get("HTTP_REFERER")
    url = request.build_absolute_uri(origin + "?token=" + token.jwt())
    return 200, URL(url=url)


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


@router.post("/use_token", url_name="use_token")
def use_link(request, token: str, link_password: SecretStr, new_password: SecretStr):
    decoded_token = decode(token)
    token_id = decoded_token.get("jti")
    request_token = RequestToken.objects.get(id=token_id)

    use_token(request_token, request)
    hashed_password = get_password_hash(link_password)
    if hashed_password != request_token.scope:
        raise Http404("Unauthorized")

    sponsor_id = request_token.data.pop("sponsor_id")

    user, created = User.objects.get_or_create(**request_token.data)
    user.set_password(new_password.get_secret_value())
    user.groups.add(user_models.recipient_group)
    user.save()

    refferal, created = user_models.Referral.objects.get_or_create(
        sponsor_id=sponsor_id, recipient=user
    )

    if not user_models.is_recipient(user):
        raise Http404("Unauthorized")

    jwt_token = jwt.create_access_token(verified_user=user)
    verified_user = auth_schemas.UserSchema.from_orm(user)

    return auth_schemas.AuthorizationResponse(user=verified_user, token=jwt_token)
