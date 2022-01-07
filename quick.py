from fusionauth.fusionauth_client import FusionAuthClient

API_KEY = "5BHOqtSiyelxUy5QwgdDsA7e81GIju1JITgDaG-PlIypwlcDz8sy1scv"
APP_ID = "109d1882-2531-40e2-8330-b49328c0028c"

client = FusionAuthClient(API_KEY, "http://localhost:9011")

USERNAME = "Kevin McGee 2"


user_request = {
    "sendSetPasswordEmail": False,
    "skipVerification": True,
    "user": {"username": USERNAME, "password": "password"},
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
    "loginId": USERNAME,
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
