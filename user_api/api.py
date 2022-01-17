from ninja import Router, Schema
from typing import List
from django.shortcuts import get_list_or_404
from . import models
from django.contrib.auth.models import User


router = Router()


class RecipientOutput(Schema):
    id: int
    username: str
    first_name: str
    last_name: str


@router.get("recipients", url_name="list_recipients", response=List[RecipientOutput])
def list_recipients(request, sponsor_id: int):
    # recipients_list = get_list_or_404(models.Referral, sponsor_id=sponsor_id)
    recip_ids = models.Referral.objects.filter(sponsor_id=sponsor_id).values_list("recipient_id")
    recipients_list = models.User.objects.filter(pk__in=recip_ids)
    return recipients_list
