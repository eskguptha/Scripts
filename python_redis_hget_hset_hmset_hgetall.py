from datetime import datetime,timedelta
from random import randrange
import time
import redis
import json
"""
Create Test Data
Create datewise account_cache
Merge Datewise account_cache into Oneaccount
HGET, HSET, HMSET, HGETALL, SCAN etc
"""

redis_con = redis.StrictRedis(host='localhost', port=6379, db=0)
NO_OF_ACCOUNTS = 10

def random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


def create_cache(account_number, timestamp_obj, app_id):
    account_number = str(account_number)
    current_date_str = timestamp_obj.strftime("%Y%m%d")
    account_data = redis_con.hget("account_list_{0}".format(current_date_str), account_number)
    if not account_data:
        account_data = {"timestamp" : timestamp_obj.isoformat(), "app_id" : app_id}
        redis_con.hset("account_list_{0}".format(current_date_str),account_number, json.dumps(account_data))
    pass

def merge_cache():
    key_pattern = "account_list_*"
    date_wise_accounts = redis_con.scan_iter(key_pattern)
    for each_date in date_wise_accounts:
        account_data = redis_con.hgetall(each_date)
        redis_con.hmset("account_list", account_data)
        redis_con.delete(each_date)
    pass


if __name__ == '__main__':
    for i in range(1, NO_OF_ACCOUNTS):
        start_date = datetime.strptime('1/11/2018 00:00:00', '%d/%m/%Y %H:%M:%S')
        end_date = datetime.strptime('24/11/2018 23:59:00', '%d/%m/%Y %H:%M:%S')
        timestamp_obj = random_date(start_date, end_date)
        account_number = i
        app_id = i 
        create_cache(account_number, timestamp_obj, app_id)
    merge_cache()
