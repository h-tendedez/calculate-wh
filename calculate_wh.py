import csv
import re
import time
import sys
import datetime
import logging
import logging.handlers
import csv
import pandas as pd
# for pyplot
import numpy as np
import matplotlib.pyplot as plt
import datetime
import time


## Insert your log, amend your seperator and if a header is present
data = pd.read_csv('yourlog.log', sep=" ", header = None)

## Remove any NaNs
data = data.dropna()

## Name each column
data.columns = ["Date", "Time", "Plug", "MAC Address", "Watts", "At", "UNIX Time" ]

# Remove nanoseconds from time (not needed for this process)
data['Time'] = [x.split(',')[0] for x in data['Time']]

## Combine date, time and watts.
data["DateTime"] = data["Date"].map(str) + " " + data["Time"]

data["DateTime"] = pd.to_datetime(data['DateTime'])

data["DateTimeWatts"] = data["Date"].map(str) + " " + data["Time"].map(str) + " " + data["Watts"].map(str)


## Get dates from log
uniqueDates = np.unique(data.Date)

print(uniqueDates)

## Method to calc Wh
def calcWh(self, uniqueDates):
    totalinWh = []
    index = 0
    i = 0
    dates = 0

    for i in range(len(uniqueDates)):

        total = 0
        ## Get days
        thisDate = data[data['Date'].isin([uniqueDates[dates]])]

        thisDate = thisDate.reset_index(drop=True)
        #print((len(thisDate)-1))
        for k in range(len(thisDate)-1):

            ## Get Watts
            value1 = thisDate.Watts[k]
            value2 = thisDate.Watts[k+1]

            totalWatts = (value1 + value2)/2
            ## Get Times
            time1 = thisDate.DateTime[k]

            time2 = thisDate.DateTime[k+1]

            ## Calculate difference in time
            time = pd.Timedelta(time2 - time1).seconds
            #print(time, totalWatts)

            sumtotal = time * totalWatts

            total = total + sumtotal
            #print(time, sumtotal, total)
        #print(min(wtts),max(wtts))
        theDay = uniqueDates[index]

        total = total/3600

        result = [theDay, total]

        totalinWh.append(result)

        index = index + 1

        dates = dates + 1

    return totalinWh


totalinWh = calcWh(data.DateTimeWatts, uniqueDates)

## unpack list
dates, watts = zip(*totalinWh)

print(totalinWh)
