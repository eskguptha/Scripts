from datetime import datetime
import pandas as pd
import redis
import ast
import json
import pickle
from random import randrange
from datetime import timedelta
import time

"""
SADD, SISMEMBER,SMEMBERS, SREM,DELETE
"""
redis_con = redis.StrictRedis(host='localhost', port=6379, db=0)
NO_OF_ACCOUNTS = 1000
DELETE_HOURS = [12]

def random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


def load_data(account_number, timestamp_obj, app_id):
	current_date_str = timestamp_obj.strftime("%Y%m%d")
	current_hour_str = timestamp_obj.strftime("%Y%m%d%H")
	account_log = {
		"account_number" : account_number,
		"app_id" : app_id,
		"timestamp" : timestamp_obj
		}
	if not redis_con.sismember(current_date_str, account_number):
		redis_con.sadd(current_date_str, account_number)
		redis_con.sadd(current_hour_str, pickle.dumps(account_log))
	else:
		pass
	# delete accounts log in DELETE HOURS
	if timestamp_obj.hour in DELETE_HOURS:
		start_time = time.process_time()
		for each_delete_hour in DELETE_HOURS:
			if each_delete_hour < 10:
				delete_hour = "{0}0{1}".format(current_date_str ,each_delete_hour)
			else:
				delete_hour = "{0}{1}".format(current_date_str, each_delete_hour)
			account_log_list = redis_con.smembers(delete_hour)
			account_number_list = [pickle.loads(each_account_log)['account_number'] for each_account_log in account_log_list]
			if account_number_list:
				for each_account_number in account_number_list:
					redis_con.srem(current_date_str, each_account_number)
				redis_con.delete(delete_hour)
			total_elapsed_time = time.process_time() - start_time
			print (total_elapsed_time)
	pass


if __name__ == '__main__':
	for i in range(NO_OF_ACCOUNTS):
		start_date = datetime.strptime('24/11/2018 00:00:00', '%d/%m/%Y %H:%M:%S')
		end_date = datetime.strptime('24/11/2018 23:59:00', '%d/%m/%Y %H:%M:%S')
		timestamp_obj = random_date(start_date, end_date)
		account_number = i
		app_id = i 
		load_data(account_number, timestamp_obj, app_id)
