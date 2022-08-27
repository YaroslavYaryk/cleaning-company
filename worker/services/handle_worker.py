from worker.models import WorkerShift


def get_shift_by_id(shift_id):
    return WorkerShift.objects.get(id=shift_id)
