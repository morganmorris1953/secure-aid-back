from fusionauth.fusionauth_client import FusionAuthClient

API_KEY = "oQHNGcV4yLsKXjYCEiF4Mhlp-u3YBLH7KyGrJANvJasJkANLpGb83pol"
CLIENT_ID = "1b0afe15-af4d-4e77-a8b5-bae48605c5d9"
APP_ID = "47505e1b-18d8-4aaf-8908-2d415da10d31"

client = FusionAuthClient(API_KEY, "http://localhost:9011")

EMAIL = "alksdjflksajdlfkjslfak"

user_request = {
    "sendSetPasswordEmail": False,
    "skipVerification": True,
    "user": {"username": EMAIL, "password": "password"},
}

client_response = client.create_user(user_request)

if client_response.was_successful():
    print(client_response.success_response)
    code = client_response.success_response
    print("good")
else:
    print(client_response.error_response)
    print("bad")

user_request = {
    "applicationId": APP_ID,
    "loginId": EMAIL,
    "state": {
        "client_id": APP_ID,
        "redirect_uri": "https://localhost:8000/callback",
        "response_type": "code",
        "scope": "openid",
        "state": "CSRF123",
    },
}

client_response = client.start_passwordless_login(user_request)

if client_response.was_successful():
    print(client_response.success_response)
    code = client_response.success_response
    print("good")
else:
    print(client_response.error_response)
    print("bad")

from pprint import pprint

client_response = client.passwordless_login(code)

if client_response.was_successful():
    pprint(client_response.success_response)
    print("good")
else:
    print(client_response.error_response)
    print("bad")


# Retrieve a user by email address

# client_response = client.retrieve_user_by_email("dgnsrekt@pm.me")
# if client_response.was_successful():
#     print(client_response.success_response)
# else:
#     print(client_response.error_response)
