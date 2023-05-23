import datetime
import time


def check_time():
   
   t1 = datetime.datetime.now()
   time.sleep(60)
   t2 = datetime.datetime.now()
   max_timeout = datetime.timedelta(0, 0, 0, 0, 5, 0, 0)
   print(t1.time())
   print(t2.time())
   print(max_timeout)
   print(t2 - t1)
   t3 = t2 - t1
   print(t3 > max_timeout)
check_time()
