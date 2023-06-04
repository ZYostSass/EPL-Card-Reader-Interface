import datetime
import time
import csv

#totally temporary way of saving the time. I don't know if we want to add something to our databaase for this or not. 
def saveTime(timestamp):
    with open('web_app/timestamp.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        time = [timestamp]
        writer.writerow(time)

def checkTime():
    with open('web_app/timestamp.csv', 'r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            return row

def set_time():
    
    saveTime(time.time())    

def betterTimeout():
    
    test_max = 20
    savedtime = checkTime()
    
    if (time.time() - float(savedtime[0])) > test_max:
        print("log user out")
        return False
    else:
        saveTime(time.time())
        print("just in time!")
        return True
    
betterTimeout()
#timeout() 