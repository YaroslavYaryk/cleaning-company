from copyreg import constructor
import json

from worker.models import WorkerShift
from work.models import RoomWork, Room, Work, WorkerJob
from django.utils.text import slugify
import re
from datetime import datetime, date


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


def get_all_shift_works(date_input):
    print(date_input)
    if date_input == str(-1):
        find_date = date.today()
    else:
        find_date = datetime.strptime(date_input, "%d-%m-%y")

    return Work.objects.filter(worker_shift__date=find_date)


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


def get_free_rooms_for_work(worker_jobs_shift):
    taken_rooms = {
        room.room_work.room.slug for room in worker_jobs_shift.worker_job.all()
    }
    return json.dumps(list(taken_rooms))


def delete_worker_room_work(shift_id, room_id):

    shift_work = Work.objects.get(worker_shift__id=shift_id)
    shift_work.worker_job.filter(room_work__room__id=room_id).delete()


def delete_old_works(shift, taken_rooms):
    for room in taken_rooms:
        shift.worker_job.filter(room_work__room__name=room).delete()


def update_existed_works(shift, data):
    shift_work = Work.objects.get(worker_shift=shift)
    taken_rooms = list(
        {room.room_work.room.slug for room in shift_work.worker_job.all()}
    )
    delete_old_works(shift_work, taken_rooms)
    room_works = [slugify(elem) for elem in get_room_work_slugs(data)]
    # print(room_works)
    add_room_works_to_shift(shift_work, room_works)


def delete_all_shift_works(shift):
    shift.worker_job.all().delete()


def delete_whole_worker_shift(shift_id):
    shift_work = Work.objects.get(worker_shift__id=shift_id)
    delete_all_shift_works(shift_work)
    shift_work.worker_shift.delete()


def get_searched_shifts(worker_email):
    return Work.objects.filter(worker_shift__user__email=worker_email)


def jsonify_users(users):
    return json.dumps([us.email for us in users])


def get_shift_by_id(shift_id):
    return WorkerShift.objects.get(pk=shift_id)