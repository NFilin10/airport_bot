import datetime
# date = input('Sisesta kuupaev (mm.dd.yyyy):')

def kuupaev_kontroll(date):
    try:
        datetime.datetime.strptime(date, '%m.%d.%Y')
        result = True
    	
    except ValueError:
        result = False
    
    return result

#print(kuupaev_kontroll(date))

date1 = '12:05'
date2 = '19:32'



def time_difference_minutes(date1,date2): 
    format = '%H:%M'
 
    datetime1 = datetime.datetime.strptime(date1, format)
    datetime2 = datetime.datetime.strptime(date2, format)
    
    seconds = (datetime2 - datetime1).total_seconds()
    minutes = int(seconds / 60)
    
    return(minutes)

print(time_difference_minutes(date1,date2))



