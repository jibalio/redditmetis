import datetime
import pytz

def get_date_now():
    return datetime.datetime.now(pytz.timezone("Asia/Manila"))
