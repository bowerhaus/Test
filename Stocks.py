import matplotlib.pyplot as plt
import matplotlib.dates as dt
import datetime
from yahoo_finance import Share

share = Share('AAPL')
name = share.get_name()

print(name)