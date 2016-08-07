#!/usr/local/bin/python

import numpy as np
import h5py as h5
import gc
import aotLib
from colorama import Fore, Back, Style
from aotConf import aquaPath
from aotConf import aeronetPath
from sys import argv

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
#aqua path work
#
yearMonth=argv[1]
#yearMonth='201401'
inputAquaDataPath, outputAquaDataPath=aquaPath()
#filePath=inputAquaDataPath+'/'+yearMonth+'/'
#filePath=inputAquaDataPath+'/'+yearMonth+'Nasa'+'/'
filePath=inputAquaDataPath+'/Nasa'+yearMonth+'/'

processId=argv[2]

rec='nasa'
satellite='aqua_'+rec



#---------------------------------
print filePath

#---------------------------------
# geometric parameters
#
nameStationArr=[]
aeronetLatArr=[]
aeronetLonArr=[]

inputAeronetDataPath,outputAeronetDataPath=aeronetPath()

dataLev = argv[3]

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
lenList=[]
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

lenPathList, aerosolFilePathList=aotLib.getAotAquaFileList(filePath)

#aerosolFilePathList=['/Users/josedias/Documents/aotData/aqua/Nasa201410/MYD04_L2.A2014279.1830.051.2014283080904.h5']

#for i in  range(len(aerosolFilePathList)):
#	print aerosolFilePathList[i]


for aotFilePath in aerosolFilePathList:

	print aotFilePath
	fileName=aotFilePath.split('/')[-1]


	if rec == 'dsa':
		idFileName=fileName.split('.')[1]
		#print idFileName

		year='20'+idFileName[:2]
		julianDay=idFileName[2:5]
		hour=idFileName[5:7]
		minute=idFileName[7:9]

	else:
	
		idFileName=fileName.split('.')
		#print idFileName

		year=idFileName[1][1:5]
		julianDay=idFileName[1][5:]
		hour=idFileName[2][:2]
		minute=idFileName[2][2:]

	
	decimalTime=aotLib.getDecimalTimeMinute(minute,hour)
	time=float(julianDay)+round(decimalTime,5)

	#print year, time
#	print nameStationArr

	
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
