import datetime
import time
import csv



#totally temporary way of saving the time. I don't know if we want to add something to our databaase for this or not. 
def saveTime(timestamp):
    with open('timestamp.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        time = [timestamp]
        writer.writerow(time)

def checkTime():
    with open('timestamp.csv', 'r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            return row
    
#this should probably work like a wrapper of some kind on the different routes.  
def timeout():
   
    saveTime(datetime.datetime.now()) 
    print(checkTime())
    temp = checkTime()
    print(temp[0])
    save = datetime.datetime(temp[0]) 
   # user_active_time = datetime.datetime.now()
    print(user_active_time,"initial user activity")
    
    time.sleep(10)
    
    current_time = datetime.datetime.now()
    print(current_time, "user activity after some delay")
    
    if (current_time-user_active_time) > test_max:
        print("logging user out")  
        #attach this to logout fn in views. 
    else:
        user_active_time = datetime.datetime.now()
        print(user_active_time)


#==================================================

max_inactive_time = datetime.timedelta(0, 300, 0, 0)
test_max = 10

def betterTimeout():
    currentTime = time.time()
    saveTime(time.time())
    savedtime = checkTime()
    print(savedtime[0])
    print(currentTime, "time since epoch when user did some activity")
    time.sleep(10)
    if (time.time() - float(savedtime[0])) > test_max:
        print("log user out")
    else:
        print("just in time!")
    
betterTimeout()
#timeout() 