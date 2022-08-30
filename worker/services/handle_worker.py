from worker.models import WorkerShift
from work.models import Work, WorkerJob


def get_shift_by_id(shift_id):
    return WorkerShift.objects.get(id=shift_id)


def get_shift_by_user(user):
    return Work.objects.filter(worker_shift__user=user)


def done_shift_work(worker_job_id):

    worker_job = WorkerJob.objects.get(pk=worker_job_id)
    worker_job.done = True
    worker_job.save()
