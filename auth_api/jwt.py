from datetime import datetime, timedelta
from typing import Optional

from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from jose import JWTError, jwt
from ninja.security import HttpBearer
from pydantic import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from . import schemas


JWT_SECRET = settings.JWT_SECRET
JWT_ALGORITHM = settings.JWT_ALGORITHM


def create_access_token(*, verified_user: User) -> schemas.JsonWebToken:
    refresh_token = RefreshToken.for_user(verified_user)

    return schemas.JsonWebToken(
        access_token=str(refresh_token.access_token),
        refresh_token=str(refresh_token),
        token_type="Bearer",
    )


def verify_access_token(*, token: str):
    data = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
    return data.get("user_id")


class InvalidToken(Exception):
    pass


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            user_id = verify_access_token(token=token)
            verified_user = get_object_or_404(User, id=user_id)
            return verified_user
        except (ValidationError, JWTError, User.DoesNotExist) as e:
            raise InvalidToken
