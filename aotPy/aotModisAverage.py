import pandas as pd
import numpy as np
import h5py as h5

import pickle
import datetime
import calendar 
from mpi4py import MPI
from sys import argv
from colorama import Fore, Back, Style

import aotLib
from aotConf import aotModis3k
#import aotPostProcess
import extractLib


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

def strRank(rank):

        if rank < 9:
                strRank = '0' + str(rank + 1)

        else:
                strRank = str(rank + 1)

        return strRank


#--main code --#

comm = MPI.COMM_WORLD

size = comm.Get_size()
rank = comm.Get_rank()

year = argv[1]

try:
	month = argv[2]

except:
	month = strRank(rank)

satellite = 'Modis'
sensor = 'modis'

print 'Extracting %s data, month %s from %s' % (satellite, month, str(size))

inputAquaDataPath, outputAquaDataPath = aotModis3k()

pathOut = outputAquaDataPath + '/' + str(year) + '/'
filePath = inputAquaDataPath + '/' + str(year) + '/'

lenList, aotFileList = aotLib.getAotAquaFileList(filePath)
aotFileList = sorted(aotFileList)
#leastFile = aotFileList[-1]

beginLatReg, endLatReg = -60., 20.
beginLonReg, endLonReg = -96., -13.

lonGrid = np.arange(endLonReg, beginLonReg, -3./111.2)
latGrid = np.arange(beginLatReg, endLatReg, 3./111.2)

xx, yy = np.meshgrid( lonGrid, latGrid)

aotPlus = np.zeros((xx.shape[0], xx.shape[1]), float)
aotCount = np.zeros((xx.shape[0], xx.shape[1]), float)
aotGridded=np.zeros((xx.shape[0], xx.shape[1]), float)

beginDay, endDay = getMonthFirstAndLastDay(year,month)

aotFileList = getFileBetween2Days(beginDay, endDay, aotFileList)

for aotFilePath in aotFileList: 

        try:
            aerosolFile=h5.File(aotFilePath,'r')
            aeroOptDep=np.array(aerosolFile['/mod04/Data Fields/Optical_Depth_Land_And_Ocean'])

            lat=np.array(aerosolFile['/mod04/Geolocation Fields/Latitude'])
            lon=np.array(aerosolFile['/mod04/Geolocation Fields/Longitude'])
            
            aerosolFile.close()
            
            while True:

                lat,lon,aeroOptDep,parameter=aotLib.removeValues(0.,lat,lon,aeroOptDep)
    
                if parameter==0:

                    break
                    
            while True:

                lat,lon,aeroOptDep,parameter=aotLib.removeValues(-999.0,lat,lon,aeroOptDep)
    
                if parameter==0:

                    break

            aeroOptDep=aeroOptDep*10**(-3)           

            rowMin, rowMax, colMin, colMax=aotLib.getRegionIndexMatrix(beginLatReg, endLatReg, lat, beginLonReg,\
									endLonReg, lon)
            
            lat = aotLib.getNewMatrix(rowMin, rowMax, colMin, colMax, lat)
            lon = aotLib.getNewMatrix(rowMin, rowMax, colMin, colMax, lon)       
        
            aeroOptDep = aotLib.getNewMatrix(rowMin, rowMax, colMin, colMax, aeroOptDep)

            lat = np.ma.masked_where(lat>=endLatReg, lat)
            lat = np.ma.masked_where(lat<=beginLatReg, lat) 

            lon = np.ma.masked_where(lon<=beginLonReg,lon)
            lon = np.ma.masked_where(lon>=endLonReg, lon)
        
            deltaY = 3.
            yDegRes = extractLib.DoDegResolutionY(deltaY)
            yIndex = np.array((lat - beginLatReg) / yDegRes, int)

            deltaX = 3.
            xDegRes = extractLib.DoDegResolutionX(deltaX)
            xIndex = np.array((endLonReg - lon) / xDegRes, int)
                    
            aotGridded[yIndex,xIndex]=aeroOptDep
            
            aotGridded = np.ma.masked_where(aotGridded <= 0, aotGridded)
            np.ma.set_fill_value(aotGridded,0) 
            aotGridded = np.ma.filled(aotGridded)
            
            aotPlus = aotPlus + aotGridded
                       
            aotGriddedTemp = aotGridded*1
            aotGriddedTemp[aotGriddedTemp > 0] = 1
            aotCount = aotCount + aotGriddedTemp

	    #print aotFilePath    


            
        except:# IOError:
           pass
            
aotCount = np.ma.masked_where(aotCount==0, aotCount)
    
aotMean =(aotPlus / aotCount)
flagMean=np.zeros_like(aotMean)
np.ma.set_fill_value(flagMean,0)
aotGridded = np.ma.filled(aotGridded)
    
flagMean[aotMean != 0.] = 15
flagMean = np.array(flagMean, int)

tempFile = pathOut + 'aotMean' + satellite + year + month + '.p'    
pickle.dump(aotMean, open(tempFile, 'wb'))

tempFlagFile = pathOut + 'aotFlag' + satellite + year + month + '.p'
pickle.dump(flagMean, open(tempFlagFile, 'wb'))


print(Fore.RED + 'Extraction %s data finished, month %s from %s' % (satellite, month, str(size)))
print(Style.RESET_ALL)

print #print 'mean', np.mean(aotMean)
        
