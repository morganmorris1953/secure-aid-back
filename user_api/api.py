from ninja import Router, Schema
from typing import List
from django.shortcuts import get_list_or_404
from . import models


router = Router()


class RecipientOutput(Schema):
    id: int
    sponsor_id: int
    recipient_id: int


@router.get("recipients", url_name="list_recipients", response=List[RecipientOutput])
def list_recipients(request, sponsor_id: int):
    recipients_list = get_list_or_404(models.Referral, sponsor_id=sponsor_id)
    return recipients_list
