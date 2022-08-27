from copyreg import constructor
import json
from work.models import RoomWork, Room, Work, WorkerJob
from django.utils.text import slugify
import re


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


def get_room_work_slugs(data):

    keys = "/".join(data.keys())
    template = r"work_Select_[0-9][0-9]?[0-9]?[0-9]?[0-9]?[0-9]?"
    proper_keys = re.findall(template, keys)
    a = []
    for i in proper_keys:
        a += data.getlist(i)
    return a


def create_work(shift):
    return Work.objects.create(worker_shift=shift)


def add_room_works_to_shift(work, room_works):

    for room_work in room_works:
        room_work = RoomWork.objects.get(slug=room_work)
        work.worker_job.add(WorkerJob.objects.create(room_work=room_work))


def get_all_shift_works():
    return Work.objects.all()


def get_worker_jobs_shift(shift_id):
    return Work.objects.get(worker_shift__id=shift_id)


def get_works_for_category(worker_jobs_shift):

    work_dict = {}
    for work in worker_jobs_shift.worker_job.all():
        room = work.room_work.room.name
        if work_dict.get(room):
            work_dict[room] += [work.room_work.name]
        else:
            work_dict[room] = [work.room_work.name]
    return work_dict
