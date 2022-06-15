import time
from calendar import timegm


def epoch_from_iso(iso_time: str) -> int:
    utc_time = time.strptime(iso_time, "%Y-%m-%dT%H:%M:%S.%fZ")
    epoch_time = timegm(utc_time)

    return epoch_time