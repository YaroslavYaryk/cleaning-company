from datetime import timedelta, datetime
from django import template
from work.models import RoomWork, Room
from random import randint

register = template.Library()


@register.filter
def room_component_id(room_id):
    # you would need to do any localization of the result here
    return f"room_component_{room_id}"


@register.filter
def room_components(room_id):
    # you would need to do any localization of the result here
    return RoomWork.objects.filter(room__id=room_id)


@register.filter
def room_components_by_name(room_name):
    # you would need to do any localization of the result here
    return RoomWork.objects.filter(room__name=room_name)


@register.filter
def id_by_name(room_name):
    # you would need to do any localization of the result here
    return Room.objects.get(name=room_name).id


@register.filter
def random_number(string):
    return f"{string}{randint(0,100000)}"
