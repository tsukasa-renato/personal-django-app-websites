from django.utils import timezone
from tzlocal import get_localzone
import pytz
import locale


# https://docs.djangoproject.com/en/3.0/topics/i18n/timezones/
def custom_datetime(datetime, tz=str(get_localzone())):
    timezone.activate(pytz.timezone(tz))
    current_tz = timezone.get_current_timezone()
    return current_tz.normalize(datetime)


def money_format(money, currency):
    money = float(money)
    locale.setlocale(locale.LC_MONETARY, currency)
    return locale.currency(money, grouping=True)
