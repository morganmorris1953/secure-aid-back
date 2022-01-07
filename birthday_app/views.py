from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from fusionauth.fusionauth_client import FusionAuthClient


def get_or_create_user(user_id, request):
    user = User.objects.filter(username=user_id).first()

    if not user:
        user = User(username=user_id)
        user.save()

    return user


def get_fusion_auth_client():
    return FusionAuthClient(settings.FUSION_AUTH_API_KEY, settings.FUSION_AUTH_BASE_URL)


def user_login_ok(request):
    client = get_fusion_auth_client()

    code = request.GET.get("code")

    if not code:
        print("code not found")
        return False

    try:
        redirect_url = request.build_absolute_uri(reverse("dashboard"))
        response = client.exchange_o_auth_code_for_access_token(
            code, settings.FUSION_AUTH_APP_ID, redirect_url, settings.FUSION_AUTH_CLIENT_SECRET
        )

        if response.was_successful():
            access_token = response.success_response["access_token"]
            user_id = response.success_response["userId"]
            get_or_create_user(user_id, request)
            return user_id
        else:
            print(response.error_response)
            return False

    except Exception as e:
        print(e)
        raise e


def get_login_url(request):
    redirect_uri = request.build_absolute_uri(reverse("dashboard"))
    login_url = f"{settings.FUSION_AUTH_BASE_URL}/oauth2/authorize?client_id={settings.FUSION_AUTH_APP_ID}&redirect_uri={redirect_uri}&response_type=code"
    # login_url = login_url.format(settings.FUSION_AUTH_BASE_URL, settings.FUSION_AUTH_APP_ID)

    return login_url


class HomeView(View):
    def get(self, request):
        num_user = User.objects.count()
        login_url = get_login_url(request)
        return render(
            request, "birthday_app/home.html", {"login_url": login_url, "num_user": num_user}
        )


class DashboardView(View):
    def get(self, request):
        user_id = user_login_ok(request)

        if not user_id:
            login_url = get_login_url(request)
            return redirect(login_url)

        birthday = None
        user = None

        try:
            client = get_fusion_auth_client()
            response = client.retrieve_user(user_id)

            if response.was_successful():
                user = response.success_response
            else:
                print(response.error_response)
        except Exception as e:
            print("couldn't get user")
            print(e)
            raise e

        return render(request, "birthday_app/dashboard.html", {"birthday": 1})
