from datetime import datetime


def unix_to_timestamp(unix_stamp):
    timestamp = datetime.utcfromtimestamp(unix_stamp).strftime('%d.%m.%Y %H:%M')
    return timestamp





