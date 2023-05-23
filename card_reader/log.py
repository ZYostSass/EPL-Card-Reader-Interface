import csv
import datetime 
from database.class_models import *
from database.user_options import add_new_user, remove_user

filename = 'log.csv'

#run this when appending data to logfile. 
def logFile(data):
   with open('log.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    #fake data
    fakedata = ['fname', 'lname', 'psuid', 'userid', data,  datetime.date.today()]
    
    #need to add call to database to grab correct info, then create writable object for writer. 
    writer.writerow(fakedata)
        


#run this if the log file is empty        
def initLog():
    field = ['fname' , 'lname', 'PSUID', 'CardNumber', 'date/time']
    
    exampleData = ['John', 'Doe', '123123', '123123', '123123', 'datetime' ] 
    
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(field)
        csvwriter.writerow(exampleData)
        
def main():
    initLog()
    logFile('12345')

if __name__ == "__main__":
    main()