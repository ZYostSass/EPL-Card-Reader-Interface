import csv
import datetime 
from database.class_models import *
from database.user_options import add_new_user, remove_user

filename = 'log.csv'

#run this when appending data to logfile. 
def logFile(data):
   with open('CardReaderOutputLog.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    #fake data
    fakedata = [ data,  datetime.date.today()]
    writer.writerow(fakedata)
    
    f.close()
        


#initializes log with appropriate information as header
def initLog():
    field = ['CardNumber', 'date/time']
    
    exampleData = ['123123', 'datetime' ] 
    
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(field)
        csvwriter.writerow(exampleData)
    
    csvfile.close()
       
       
##print to console.  
def printLog():
    
    print("=====Card Reader Rutput Log======")
    
    with open('log.csv', 'r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
           print(row) 
            
            
#run all available functions (debugging) 

