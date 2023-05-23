import datetime
import time
from views import logout


max_inactive_time = datetime.timedelta(0, 300, 0, 0)
test_max = datetime.timedelta(0, 10, 0, 0)

def timeout():
    
    user_active_time = datetime.datetime.now()
    print(test_max, "max time delta") 
    print(user_active_time,"initial user activity")
    time.sleep(10)
    current_time = datetime.datetime.now()
    print(current_time, "user activity after some delay")
    
    if (current_time-user_active_time) > test_max:
        print("logging user out")  
    else:
        user_active_time = datetime.datetime.now()
        print(user_active_time)
   
   
   
timeout() 