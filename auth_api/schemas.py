import urllib

from ninja import Field, Schema
from pydantic import HttpUrl, validator
from typing import List, Optional


class JsonWebToken(Schema):
    access: str
    refresh: str
    token_type: str


class UserSchema(Schema):
    username: str
    first_name: str
    last_name: str
    email: str


class VAGovProfile(Schema):
    sub: str
    name: str
    locale: str
    preferred_username: str
    given_name: Optional[str]
    middle_name: Optional[str]
    family_name: Optional[str]
    veteran_status: str
    comfirmed_veteran: bool = Field(False, alias="veteran_status")
    zoneinfo: str
    email: str
    email_verified: bool
    updated_at: int

    @validator("comfirmed_veteran", pre=True)
    def check_veteran_status(cls, value):
        if value == "confirmed":
            return True
        return False

    def to_military_bridge_profile(self):
        return UserSchema(
            username=self.preferred_username,
            email=self.email,
            first_name=self.given_name,
            last_name=self.family_name,
        )


class VAGovToken(Schema):
    access_token: str
    id_token: str
    refresh_token: str
    token_type: str
    scope: List[str]
    expires_in: int
    state: str
    expires_at: float


class URL(Schema):
    url: HttpUrl


class AuthorizationResponse(Schema):
    user: UserSchema
    token: JsonWebToken
