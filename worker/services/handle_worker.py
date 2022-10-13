from worker.models import WorkerShift, FreeDates
from work.models import Work, WorkerJob
from accounts.models import User
from datetime import datetime, date
from accounts.services import handle_user
from datetime import datetime
from worker.api.services import handle_api

DATE_FORMAT = "%m-%d-%y"


def get_shift_by_id(shift_id):
    return WorkerShift.objects.get(id=shift_id)


def get_shift_by_user(user, date_input):

    if date_input == str(-1):
        find_date = date.today()
    else:
        find_date = datetime.strptime(date_input, "%d-%m-%y")

    return Work.objects.filter(worker_shift__user=user, worker_shift__date=find_date)


def done_shift_work(worker_job_id):

    worker_job = WorkerJob.objects.get(pk=worker_job_id)
    worker_job.time = datetime.now()
    worker_job.done = True
    worker_job.save()


def get_free_setup_users(user):
    return User.objects.exclude(email=user.email).exclude(admin=True)


def add_dates_to_free_dates(obj, dates):
    new_dates = dates.split("to")
    if len(new_dates) == 2:
        obj.start_date = datetime.strptime(new_dates[0].strip(), DATE_FORMAT)
        obj.end_date = datetime.strptime(new_dates[1].strip(), DATE_FORMAT)
    else:
        print("here", dates)
        obj.start_date = datetime.strptime(new_dates[0], DATE_FORMAT)
        obj.end_date = datetime.strptime(new_dates[0], DATE_FORMAT)

    obj.save()


def get_all_free_dates(user):
    return FreeDates.objects.filter(user=user)


def get_dree_day_by_id(free_date_id):
    return FreeDates.objects.get(id=free_date_id)


def get_data_list(free_date):
    return f"""
        {free_date.start_date.strftime("%m-%d-%y")} to {free_date.end_date.strftime("%m-%d-%y")}
    """


def is_avaluable_date_for_worker(data):
    dates = data.get("datepicker")
    new_dates = dates.split("to")
    if len(new_dates) == 2:
        start_date = datetime.strptime(new_dates[0].strip(), DATE_FORMAT)
        end_date = datetime.strptime(new_dates[1].strip(), DATE_FORMAT)

    else:
        start_date = datetime.strptime(dates, DATE_FORMAT)
        end_date = datetime.strptime(dates, DATE_FORMAT)

    setup_worker = None
    if data.get("setup_worker"):
        setup_worker = handle_user.get_user_by_email(data.get("setup_worker"))

    user_main_works = Work.objects.filter(worker_shift__user=setup_worker)
    for elem in user_main_works:
        if start_date >= elem.worker_shift.date <= end_date:
            return True

    # user_setup_works =


def get_worker_setup_dates(user):
    return FreeDates.objects.filter(setup_worker=user)


def get_workers_free_dates():
    return FreeDates.objects.all()


def get_worker_free_dates(email):
    return FreeDates.objects.filter(user__email=email)


def approve_free_date(free_date_id):
    print("here")
    obj = FreeDates.objects.get(id=free_date_id)
    obj.approved = "True"
    obj.save()


def refuse_free_date(free_date_id):
    obj = FreeDates.objects.get(id=free_date_id)
    obj.approved = "False"
    obj.save()


def delete_free_date(pk):
    FreeDates.objects.get(pk=pk).delete()
