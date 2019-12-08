import concurrent.futures
import redis
import traceback
import time
"""
https://docs.python.org/3/library/concurrent.futures.html
The concurrent.futures module provides a high-level interface for asynchronously executing callables.
The asynchronous execution can be performed with threads, using ThreadPoolExecutor, or separate processes, using ProcessPoolExecutor. Both implement the same interface, which is defined by the abstract Executor class.

"""

redis_con = redis.Redis("127.0.0.1", 6379)

def redis_hget_all(key_name, field):
    start_time = time.time()
    data = redis_con.hget(key_name, field)
    end_time = time.time()
    return data, start_time, end_time

def redis_get(key_name):
    start_time = time.time()
    data = redis_con.get(key_name)
    end_time = time.time()
    return data, start_time, end_time
    
task_list = []
executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)

exc_res_1 = executor.submit(redis_get, 'department')
exc_res_2 = executor.submit(redis_hget_all, 'student', '1')
#exc_res_2 = executor.submit(redis_get, 'department')

task_list.append(exc_res_1)
task_list.append(exc_res_2)
print ("With concurrent.futures")
for each_task in task_list:
    futuer= concurrent.futures.as_completed(each_task)
    try:
        data, start_time, end_time = each_task.result()
        print (start_time, end_time, "Differences",end_time-start_time)
    except Exception as exc:
        traceback.print_exc()
print ("With out concurrent.futures")
r , start_time, end_time = redis_get("department")
print (start_time, end_time, "Differences",end_time-start_time)

r , start_time, end_time = redis_hget_all('student', '1')
print (start_time, end_time, "Differences",end_time-start_time)
