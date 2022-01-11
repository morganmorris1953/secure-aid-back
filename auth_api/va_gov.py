from django.conf import settings
from requests_oauthlib import OAuth2Session

APPLICATION_ID = settings.VA_APPLICATION_ID
API_KEY = settings.VA_API_KEY
CLIENT_ID = settings.VA_API_OATH_CLIENT_ID
CLIENT_SECRET = settings.VA_API_OATH_CLIENT_SECRET
REDIRECT_URI = settings.VA_API_OATH_REDIRECT_URI

AUTHORIZATION_URL = "https://sandbox-api.va.gov/oauth2/veteran-verification/v1/authorization"
TOKEN_URL = "https://sandbox-api.va.gov/oauth2/veteran-verification/v1/token"
USERINFO_URL = "https://sandbox-api.va.gov/oauth2/veteran-verification/v1/userinfo"


def create_session():
    scope = ["profile", "offline_access", "openid", "veteran_status.read", "email"]
    session = OAuth2Session(CLIENT_ID, scope=scope, redirect_uri=REDIRECT_URI)
    return session


def get_token_from_callback(*, code):
    session = create_session()
    token = session.fetch_token(TOKEN_URL, code=code, client_secret=CLIENT_SECRET)
    return token


def create_session_with_token(*, token):
    auto_refresh_kwargs = {"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET}
    include = {"access_token", "refresh_token", "token_type", "expires_in"}
    token = token.dict(include=include)

    session = OAuth2Session(
        client_id=CLIENT_ID, token=token, auto_refresh_kwargs=auto_refresh_kwargs
    )
    return session
