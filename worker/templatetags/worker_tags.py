from datetime import timedelta, datetime
from django import template
from work.models import RoomWork, Room
from random import randint
from accounts.models import User
import json
from worker.models import FreeDates

register = template.Library()


@register.filter
def user_name(user_id):
    if not (user_id):
        return json.dumps(None)
    try:
        print(user_id)
        user_set_up_dates = FreeDates.objects.filter(
            setup_worker__id=user_id, approved="True"
        )
        print(user_set_up_dates)
    except Exception as ex:
        print(ex)
        return json.dumps(None)

    return json.dumps({"res": user_id.id}) if user_id else json.dumps(None)
