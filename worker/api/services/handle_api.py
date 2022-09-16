from worker.models import FreeDates
from worker.services.handle_worker import DATE_FORMAT
from datetime import datetime
import json

NEW_DATE_FORMAT = "%Y-%m-%d"


def is_overlapped(range_1, time_range):
    print(max(range_1[0], time_range[0]), min(range_1[1], time_range[1]))
    return max(range_1[0], time_range[0]) <= min(range_1[1], time_range[1])


def get_taken_dates(worker_id, data):
    try:
        date1 = datetime.strptime(data["date"][0], DATE_FORMAT)
        date2 = datetime.strptime(data["date"][1], DATE_FORMAT)
    except ValueError:
        date1 = datetime.strptime(data["date"][0], NEW_DATE_FORMAT)
        date2 = datetime.strptime(data["date"][1], NEW_DATE_FORMAT)

    my_free_dates = FreeDates.objects.filter(user__id=worker_id, approved=True)
    for dates in my_free_dates:
        if is_overlapped(
            [date1, date2],
            [
                datetime.strptime(str(dates.start_date), NEW_DATE_FORMAT),
                datetime.strptime(str(dates.end_date), NEW_DATE_FORMAT),
            ],
        ):
            return [str(dates.start_date), str(dates.end_date)], "free_dates"

    my_setup_dates = FreeDates.objects.filter(setup_worker__id=worker_id, approved=True)
    for dates in my_setup_dates:
        if is_overlapped(
            [date1, date2],
            [
                datetime.strptime(str(dates.start_date), NEW_DATE_FORMAT),
                datetime.strptime(str(dates.end_date), NEW_DATE_FORMAT),
            ],
        ):
            return [str(dates.start_date), str(dates.end_date)], "setup_dates"

    return None, None
