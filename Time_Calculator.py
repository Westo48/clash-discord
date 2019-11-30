from datetime import datetime, timedelta

time_format = '%H:%M:%S'


def get_current_time():
    time_now = datetime.now()
    time_string = time_now.strftime(time_format)
    return time_string
