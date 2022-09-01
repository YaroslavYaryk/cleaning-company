from worker.models import WorkerShift, FreeDates
from work.models import Work, WorkerJob
from accounts.models import User
from datetime import datetime

DATE_FORMAT = "%m-%d-%y"


def get_shift_by_id(shift_id):
    return WorkerShift.objects.get(id=shift_id)


def get_shift_by_user(user):
    return Work.objects.filter(worker_shift__user=user)


def done_shift_work(worker_job_id):

    worker_job = WorkerJob.objects.get(pk=worker_job_id)
    worker_job.done = True
    worker_job.save()


def get_free_setup_users(user):
    return User.objects.exclude(email=user.email).exclude(admin=True)


def add_dates_to_free_dates(obj, dates):
    new_dates = dates.split("to")
    try:
        if len(new_dates) == 2:
            print(datetime.strptime(new_dates[0].strip(), DATE_FORMAT))
            obj.start_date = datetime.strptime(new_dates[0].strip(), DATE_FORMAT)
            obj.end_date = datetime.strptime(new_dates[1].strip(), DATE_FORMAT)
        else:
            obj.start_date = datetime.strptime(dates, DATE_FORMAT)
            obj.end_date = datetime.strptime(new_dates, DATE_FORMAT)

        obj.save()
    except Exception as er:
        print(er)


def get_all_free_dates(user):
    return FreeDates.objects.filter(user=user)
