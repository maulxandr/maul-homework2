#!/usr/bin/python3.5

import datetime

def get_days_to_new_year():
    now = datetime.datetime.now()
    next_year = datetime.datetime(now.year + 1, 1, 1)
    do_novogo_goda = next_year - now
    return do_novogo_goda.days
