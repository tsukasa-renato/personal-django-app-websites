from django.utils import timezone
from tzlocal import get_localzone
import pytz


def custom_datetime(datetime, tz=str(get_localzone())):
    timezone.activate(pytz.timezone(tz))
    current_tz = timezone.get_current_timezone()
    return current_tz.normalize(datetime)
