import numpy as np
import pandas as pd

import calendar
import datetime

def DoDegResolutionX(deltaX):

    earthRay = 6371.    
    #lonRes = (deltaX * 360)/ (2 * np.pi * earthRay * np.cos((lat * np.pi)/180.))
    lonRes = (deltaX * 360)/ (2 * np.pi * earthRay)

    return lonRes

def DoDegResolutionY(deltaY):
    
    earthRay = 6371
    latRes = (deltaY * 360)/ (2 * np.pi * earthRay)
    
    return latRes


def getMonthFirstAndLastDay(year,month):

    weekDayBegin, lenMonth = calendar.monthrange(int(year),int(month))
    beginDay = datetime.datetime.strptime(year+month+'01','%Y%m%d').strftime('%Y%j')
    endDay = datetime.datetime.strptime(year+month+str(lenMonth),'%Y%m%d').strftime('%Y%j')

    return beginDay, endDay


def getFileBetween2Days(beginDay,endDay,fileList):

    dataFrame = pd.DataFrame(fileList)
    dataFrame = dataFrame[(dataFrame[0].str.split('/').str[-1].str.split('.').str[1].str[1:] >= beginDay )]
    dataFrame = dataFrame[(dataFrame[0].str.split('/').str[-1].str.split('.').str[1].str[1:] <= endDay)]

    fileList = list(dataFrame[0])

    return fileList



