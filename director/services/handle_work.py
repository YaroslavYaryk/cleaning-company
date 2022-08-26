from copyreg import constructor
import json
from work.models import RoomWork, Room
from django.utils.text import slugify


def create_room_work(room, name):
    RoomWork.objects.create(room=room, name=name, slug=slugify(name))


def get_rooms_json(queryset):
    return json.dumps(
        [{"name": "------", "slug": "------"}]
        + [{"name": el.name, "slug": el.slug} for el in queryset]
    )


def get_all_rooms():

    return Room.objects.all(), get_rooms_json(Room.objects.all())


def get_room_by_id(room_id):
    return Room.objects.get(id=room_id)


def get_room_by_slug(room_slug):
    return Room.objects.get(slug=room_slug)


def get_work_for_room(room):
    return RoomWork.objects.filter(room=room)


def delete_room_work(room_work_slug):
    RoomWork.objects.get(slug=room_work_slug).delete()


def edit_or_create_room_work(room, name, idd):
    try:
        item = RoomWork.objects.get(id=idd)
        item.name = name
        item.slug = slugify(name)
        item.save()
    except Exception:
        create_room_work(room, name)


def delete_room(room_slug):
    Room.objects.get(slug=room_slug).delete()


def get_room_works_json(queryset):
    return json.dumps(
        [
            {"room_slug": el.room.slug, "name": el.name, "slug": el.slug}
            for el in queryset
        ]
    )


def get_room_works():
    return RoomWork.objects.all(), get_room_works_json(RoomWork.objects.all())
