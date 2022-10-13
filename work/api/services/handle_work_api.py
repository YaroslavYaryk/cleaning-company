from director.services import handle_work
from .constants import SHIFT_NAMES
from work.models import Work


def add_work_to_room(room, works):
    for key in works:
        handle_work.create_room_work(room, key)


def get_shift_names():
    return SHIFT_NAMES


def update_existed_works(shift, data):
    shift_work = Work.objects.get(worker_shift=shift)
    shift_work.worker_job.all().delete()
    handle_work.add_room_works_to_shift(shift_work, data)
