import pandas as pd
import numpy as np
import h5py as h5

import gc
from mpi4py import MPI
from sys import argv
from colorama import Fore, Back, Style

import aotLib
from aotConf import aeronetPath

year = argv[1]
satellite = argv[2]
sensor = argv[3]
resolution = argv[4]
dataLev = argv[5]

if sensor == 'modis' and int(resolution) == 3:

    from aotConf import aotModis3k
    inputSatPath, outputSatPath = aotModis3k()

else 

    from aotConf import aotModis
    inputPath, outputSatPath = aotModis()


def strRank(rank):

        if rank < 9:
                strRank = '0' + str(rank + 1)

        else:
                strRank = str(rank + 1)

        return strRank




def aotProcess(filePath,aotFile,julianDay,aeronetLat,aeronetLon):

	aerosolFile=h5.File(aotFile,'r')

	try:
		aeroOptDep=np.array(aerosolFile['/Optical_Depth_Land_And_Ocean'])

	except:
		aeroOptDep=np.array(aerosolFile['/mod04/Data Fields/Optical_Depth_Land_And_Ocean'])

	aeroOptDep=np.ma.masked_where(aeroOptDep<0,aeroOptDep)

	try:
		lat=np.array(aerosolFile['/Latitude'])
		lon=np.array(aerosolFile['/Longitude'])

	except:
		lat=np.array(aerosolFile['/mod04/Geolocation Fields/Latitude'])	
		lon=np.array(aerosolFile['/mod04/Geolocation Fields/Longitude'])

	aerosolFile.close()	

	while True:
		lat,lon,aeroOptDep,parameter=aotLib.removeValues(0.,lat,lon,aeroOptDep)
    
        	#print parameter
		if parameter==0:
		       break
    
	while True:
        	lat,lon,aeroOptDep,parameter=aotLib.removeValues(-999.0,lat,lon,aeroOptDep)
    
	        #print parameter
        	if parameter==0:
		        break

	
	aeroOptDep=aeroOptDep*10**(-3)



        #-----aeronet position--------
        #aeronet= -10.0,-54.5
        #aeronet=-15.729500,-56.021000
        earthRay= 6371 ## km
        length= 40 ## km

        beginLatReg,endLatReg,beginLonReg,endLonReg=aotLib.getComparisonRegion(aeronetLat,aeronetLon,length,earthRay)
        rowMin,rowMax,colMin,colMax=aotLib.getRegionIndexMatrix(beginLatReg,endLatReg,lat,beginLonReg,endLonReg,lon)

        aeroOptDep=aotLib.getNewMatrix(rowMin,rowMax,colMin,colMax,aeroOptDep)
        lat=aotLib.getNewMatrix(rowMin,rowMax,colMin,colMax,lat)
        lon=aotLib.getNewMatrix(rowMin,rowMax,colMin,colMax,lon)

	print aeroOptDep.mean()


	return aeroOptDep.mean(),aeroOptDep.std(),aeroOptDep,lat,lon


##################################
# main code
#
#---------------------------------

comm = MPI.COMM_WORLD

size = comm.Get_size()
rank = comm.Get_rank()

try:

	month = argv[6]

except:

	month = strRank(rank)


print 'Extracting $s data, month %s from %s' % (satellite, month, str(size))
#---------------------------------

pathOut = outputSatPath
filePath = inputSatPath


#---------------------------------
# geometric parameters
#
nameStationArr=[]
aeronetLatArr=[]
aeronetLonArr=[]

inputAeronetDataPath,outputAeronetDataPath=aeronetPath()

if dataLev == 'lev20':
        filePathArr=aotLib.getAeronetPathArr(inputAeronetDataPath + '/allDataL2',dataLev)

else:
        dataLev = 'lev15'
        filePathArr=aotLib.getAeronetPathArr(inputAeronetDataPath + '/allDataL15',dataLev)

nameStationArr,aeronetLatArr,aeronetLonArr=aotLib.returnAeronetCoordenateArr(filePathArr)

#print nameStationArr
#---------------------------------


#--------------------------------------
# array variables
#
#lenList=[]
aerosolFileList=[]
timeArr=np.array([])
aotMeanArr=np.array([])
aotMeanList=[]
aotStdArr=np.array([])
aotStdList=[]
aotArr40=[]
latArr40=[]
lonArr40=[]
nameStationAux=[]
#--------------------------------------



#--------------------------------------
#

lenList, aotFileList=aotLib.getAotAquaFileList(filePath)
aotFileList = sorted(aotFileList)

beginDay, endDay = getMonthFirstAndLastDay(year,month)

aotFileList = getFileBetween2Days(beginDay, endDay, aotFileList)


for aotFilePath in aotFileList:

	print aotFilePath
	fileName=aotFilePath.split('/')[-1]

	idFileName=fileName.split('.')

	year=idFileName[1][1:5]
	julianDay=idFileName[1][5:]
	hour=idFileName[2][:2]
	minute=idFileName[2][2:]

	decimalTime=aotLib.getDecimalTimeMinute(minute,hour)
	time=float(julianDay)+round(decimalTime,5)
	
	for nameStation in range(len(nameStationArr)):
	
#		print nameStationArr[nameStation]
		try:
			aotMean,aotStd,aotMatrix,latMatrix,lonMatrix=aotProcess(filePath,aotFilePath,\
str(time),aeronetLatArr[nameStation],aeronetLonArr[nameStation])
			
				
			#print aotMean

			if aotMean >=0:
				nameStationAux=nameStationAux+[nameStationArr[nameStation]]
				aotArr40=aotArr40+[aotMatrix]
				latArr40=latArr40+[latMatrix]
				lonArr40=lonArr40+[lonMatrix]

			else:
				pass

		except:
#			print "I/O error({0}): {1}".format(e.errno, e.strerror)


#		except:
			print 'Error'
			pass
#--------------------------------------


#--------------------------------------
# write data in hdf5 file
#
#	nameStationAux=['Santiago_eauchef']

	try:

	        aotLib.writeData(outputAquaDataPath,satellite,nameStationAux,year,time,aotArr40,latArr40,lonArr40)
        	timeArr=np.append(timeArr,time)

		print(Fore.YELLOW + 'DATA WROTE')
		print(Styele.RESET_ALL)


	except:
		print(Fore.RED + 'NO DATA TO WROTE')
		print(Style.RESET_ALL)
	
	#print outputAquaDataPath,satellite,nameStationAux,year,time,aotArr40,latArr40,lonArr40 
#--------------------------------------
        #aotMeanArr=aotMeanArr.reshape(len(timeArr),3)#numberStation)
        #print aotMeanArr
#       aotMeanList=aotMeanList+[aotMeanArr]
#       aotStdList=aotStdList+[aotStdArr]
        aotArr40=[]
        latArr40=[]
        lonArr40=[]
        nameStationAux=[]

try:

	aotLib.writeDataTime(outputAquaDataPath,year,timeArr,satellite,processId)

	print(Fore.YELLOW + 'TIME WROTE')
	print(Styele.RESET_ALL)

except:

	print(Fore.RED + 'NO TIME TO WRITE')
	print(Style.RESET_ALL)
