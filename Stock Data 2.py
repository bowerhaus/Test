# Relevant imports
import matplotlib.pyplot as plt
import matplotlib.dates as dt
import datetime
from yahoo_finance import Share
from statistics import mean


# Create a class to contain relevant stock values for a time period
class Bar:
    def __init__(self,open,high,low,close):
        self.Open=open
        self.High=high
        self.Low=low
        self.Close=close

# Also want a daily Bar that contain the OHLC of a stock with the date and stock symbol
class Daily_Bar(Bar):
    def __init__(self, open, high, low, close,date):
        super().__init__(open,high,low,close)
        self.Date=date

# Defining smaller functions that will become relevant in the later function
def make_string_date(date):
    return(str(date.year) + '-' + str(date.month) + '-' + str(date.day))

def get_daily_data(data):
    KeyInfo=[]
    for i in range(len(data)):
        KeyInfo.append([float(data[i]['Open']), float(data[i]['Close']), float(data[i]['High']), float(data[i]['Low'])])
    return(KeyInfo)

def create_list(x, KeyFigures):
    list=[]
    for i in range(len(KeyFigures)):
        list.append(KeyFigures[i][x])
    return(list)

def get_list(value, KeyFigures):
    list=[]
    for i in range(len(KeyFigures)):
        list.append(KeyFigures[i].__getattribute__(value))
    return(list)

# Function that produces a list of Bars for a stock from a start date to an end date
def read_daily_bars(symbol_name, start_date, end_date):
    # Turn datetime objects into strings
    str_start_date=make_string_date(start_date)
    str_end_date=make_string_date(end_date)
    print(str_end_date)
    #Fetch information on shares from yahoo_finance
    share=Share(symbol_name)
    yahoo_data=share.get_historical(str_start_date,str_end_date)

    # Create a  list of Bars for the time period
    key_figures=[]
    for i in range(len(yahoo_data)):
        key_figures.append(Daily_Bar(float(yahoo_data[i]["Open"]),float(yahoo_data[i]["High"]),float(yahoo_data[i]["Low"]),float(yahoo_data[i]["Close"]),yahoo_data[i]["Date"]))
    return(key_figures)


# Start the overall purpose function which returns the years OHLC, average
# OHLC and company name for a given symbol
def analyse_recent_year(symbol):
    # Find the date today as datetime object
    today = datetime.date.today()

    # Create date time object for last year
    last_year = today - datetime.timedelta(days=365)

    # Create a list of the OHLC daily bars ove the last year
    list_daily_bars=read_daily_bars(symbol, last_year, today)

    # Retrieve the OHLC of the stock for each day of the year
    ListOpens=get_list('Open', list_daily_bars)
    ListClose=get_list('Close', list_daily_bars)
    ListHighs=get_list('High', list_daily_bars)
    ListLows=get_list('Low', list_daily_bars)

    # Extract the OHLC for the years period
    YearOpen=ListOpens[len(ListOpens)-1]
    YearClose=ListClose[0]
    YearHigh=max(ListHighs)
    YearLow=min(ListLows)

    # Calculate the Average OHLC for the years period
    AverageOpen=mean(ListOpens)
    AverageClose=mean(ListClose)
    AverageHigh=mean(ListHighs)
    AverageLow=mean(ListLows)

    #Get Company name
    share=Share(symbol)
    share_name=share.get_name()
    # Answer a tuple, the first element is the OHLC bar for the year and the second element is the
    # average bar for the year. The third element is the share name. Tuples are nice ways to return more than one thing from a function.
    return((Bar(YearOpen,YearHigh,YearLow,YearClose),Bar(AverageOpen,AverageHigh,AverageLow,AverageClose),share_name))

# Need to convert lists of string dates to lists of dates that can be plotted
def make_list_plot_dates(list_dates):
    list_plot_dates=[]
    for i in range(len(list_dates)):
        list_plot_dates.append(dt.datestr2num(list_dates[i]))
    return(list_plot_dates)

# Want to plot the close share value for a certain time period
def plot_closes(symbol,start_date,end_date):
    # Creates a list of the daily bars for the stock
    list_daily_bars=read_daily_bars(symbol, start_date, end_date)

    # Need to create the lists for the axis
    list_dates=get_list("Date",list_daily_bars)
    list_closes=get_list("Close",list_daily_bars)
    list_plot_dates=make_list_plot_dates(list_dates)
   # Creating the plot with red line and dots for points
   # Also adding appropriate titles
    plt.plot_date(list_plot_dates,list_closes,'r-o', xdate=True)
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.title('Stock Price for '+symbol)
    plt.show()


print(analyse_recent_year("AAPL"))
plot_closes("RL",datetime.date.today()-datetime.timedelta(days=365),datetime.date.today())