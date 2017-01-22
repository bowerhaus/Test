import yahoo_finance
import datetime
from yahoo_finance import Share
from statistics import mean

def stringdate(year,month,day):
    return(str(year) + '-' + str(month) + '-' + str(day))

def getkeyfigures(data):
    keyinfo=[]
    for i in range(len(data)):
        keyinfo.append([float(data[i]['Open']),float(data[i]['Close']),float(data[i]['High']),float(data[i]['Low'])])
    return(keyinfo)

def createlist(x,keyfigures):
    list=[]
    for i in range(len(keyfigures)):
        list.append(keyfigures[i][x])
    return(list)



def getlist(value,keyfigures):
    if value=='Open':
        return(createlist(0,keyfigures))
    if value=='Close':
        return(createlist(1,keyfigures))
    if value=='High':
        return(createlist(2,keyfigures))
    if value=='Low':
        return(createlist(3,keyfigures))



def analyserecentyear(symbol):
    date=datetime.datetime.today()
    day=date.day
    month=date.month
    year=date.year
    share=Share(symbol)
    name=share.get_name()
    yearsdata=share.get_historical(stringdate(year-1,month,day),stringdate(year,month,day))
    keyfigures=getkeyfigures(yearsdata)
    listOpens=getlist('Open',keyfigures)
    listCloses=getlist('Close',keyfigures)
    listHighs=getlist('High',keyfigures)
    listLows=getlist('Low',keyfigures)
    yearopen=listOpens[len(listOpens)-1]
    yearclose=listCloses[0]
    averageopen=mean(listOpens)
    averageclose=mean(listCloses)
    yearhigh=max(listHighs)
    yearlow=min(listLows)
    averagehigh=mean(listHighs)
    averagelow=mean(listLows)
    return([yearopen,yearclose,yearhigh,yearlow,averageopen,averageclose,averagehigh,averagelow,name])

print(analyserecentyear(input("choose your symbol. ")))
