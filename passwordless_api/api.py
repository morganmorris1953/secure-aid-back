from ninja import Router
from ninja.security import HttpBearer
from django.urls import reverse_lazy, reverse

from request_token.models import RequestToken
from request_token.utils import decode
from request_token.commands import log_token_use

from django.shortcuts import render
from request_token.decorators import use_request_token
from django.http import HttpResponse

router = Router()


@router.get("/create")
def create_link(request):
    token = RequestToken.objects.create_token(
        scope="foo", login_mode=RequestToken.LOGIN_MODE_NONE, data={"affiliate_id": 1}
    )
    return request.build_absolute_uri(reverse("api-1.0.0:use_token") + "?token=" + token.jwt())


# Create your views here.
@router.get("/use_token", url_name="use_token")
def use_link(request, token):
    decoded_token = decode(token)
    print(decoded_token)
    id = decoded_token.get("jti")
    rt = RequestToken.objects.get(id=id)
    print(rt.scope)
    print(rt.data)
    rt.validate_max_uses()
    rt.authenticate(request)
    log_token_use(rt, request, 200)

    return token
