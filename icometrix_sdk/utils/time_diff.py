from datetime import datetime, timedelta, timezone


def time_difference(utc_datetime: datetime) -> timedelta:
    """
    Parses the input datetime string and logs the time difference with the current time.

    :param utc_datetime: The datetime to be compared

    Returns:
    """
    utc_datetime = utc_datetime.replace(tzinfo=timezone.utc)
    current_utc_datetime = datetime.now(timezone.utc)
    return current_utc_datetime - utc_datetime
