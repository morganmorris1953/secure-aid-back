from django.conf import settings

from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


SERVER_URL = "https://sandbox-api.va.gov/oauth2/claims/v1/authorization"

# settings.VA_API_KEY
# settings.VA_APPLICATION_ID
# settings.VA_API_OATH_CLIENT_ID
# settings.VA_API_OATH_CLIENT_SECRET
# settings.VA_API_OATH_REDIRECT_URI

# class VAGovAccount(ProviderAccount):
# def get_profile_url(self):


class VAGovProvider(OAuth2Provider):
    id = "va_gov"
    name = "VA"

    def get_default_scope(self):
        scope = ["profile", "offline_access", "openid", "veteran_status.read"]


providers.registry.register(VAGovProvider)
