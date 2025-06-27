from datetime import datetime
import pytz

def bangkok_now():
    tz = pytz.timezone("Asia/Bangkok")
    return datetime.now(tz)
