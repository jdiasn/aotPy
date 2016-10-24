import pandas as pd
import numpy as np
import h5py as h5

#import socket 
import gc
import pickle
from mpi4py import MPI
from sys import argv
from colorama import Fore, Back, Style

import datetime

import aotLib
import extractLib
from aotConf import aeronetPath
from aotConf import outputTempDataPath as tempOutputPath


year = argv[1]
month = argv[2]
satellite = argv[3]
sensor = argv[4]
resolution = argv[5]
dataLev = argv[6]

if sensor == 'modis' and resolution == '3km':

    from aotConf import aotModis3k
    inputSatPath, outputSatPath = aotModis3k()

elif sensor == 'modis' and resolution == '10kmC51':

    from aotConf import aotModisC51
    inputSatPath, outputSatPath = aotModisC51()

else: 

    from aotConf import aotModis
    inputSatPath, outputSatPath = aotModis()

def getDay(year,month,day):

        try:
                date = datetime.datetime.strptime(year+month+day, '%Y%m%d').strftime('%Y%j')

                return date

        except:
                return None

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
		aeroOptDep=np.array(aerosolFile['/mod04/Data Fields/AOD_550_Dark_Target_Deep_Blue_Combined'])

	aeroOptDep=np.ma.masked_where(aeroOptDep<0,aeroOptDep)

	try:
		lat=np.array(aerosolFile['/Latitude'])
		lon=np.array(aerosolFile['/Longitude'])

	except:
		lat=np.array(aerosolFile['/mod04/Geolocation Fields/Latitude'])	
		lon=np.array(aerosolFile['/mod04/Geolocation Fields/Longitude'])

	try:
		qualFlag = np.array(aerosolFile['/Land_Ocean_Quality_Flag'])

	except:
		qualFlag = np.array(aerosolFile['/mod04/Data Fields/AOD_550_Dark_Target_Deep_Blue_Combined_QA_Flag'])

	aerosolFile.close()	



	ind = aotLib.verifyAeronetCoordenates(aeronetLat, aeronetLon, lat, lon)
	

	if ind == True:

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
	        length= 50 ## km

	        beginLatReg,endLatReg,beginLonReg,endLonReg=aotLib.getComparisonRegion(aeronetLat,aeronetLon,length,earthRay)
	        rowMin,rowMax,colMin,colMax=aotLib.getRegionIndexMatrix(beginLatReg,endLatReg,lat,beginLonReg,endLonReg,lon)

        	aeroOptDep=aotLib.getNewMatrix(rowMin,rowMax,colMin,colMax,aeroOptDep)
	        lat=aotLib.getNewMatrix(rowMin,rowMax,colMin,colMax,lat)
		lon=aotLib.getNewMatrix(rowMin,rowMax,colMin,colMax,lon)
		qualFlag=aotLib.getNewMatrix(rowMin,rowMax,colMin,colMax,qualFlag)

		#print aeroOptDep.mean()
		#print qualFlag.shape == aeroOptDep.shape

		return aeroOptDep.mean(), aeroOptDep.std(), aeroOptDep, lat, lon, qualFlag

	else:
		return None, None, None, None, None, None

	

##################################
# main code
#
#---------------------------------

comm = MPI.COMM_WORLD

size = comm.Get_size()
rank = comm.Get_rank()

try:

	day = argv[7]

except:

	day = strRank(rank)


#print 'Extracting %s data, month %s, %s from %s' % (satellite, month, day, str(size))

#---------------------------------

pathOut = outputSatPath + '/' + str(year) + '/'
filePath = inputSatPath + '/' + str(year) + '/'


#---------------------------------
# geometric parameters
#
nameStationArr=[]
aeronetLatArr=[]
aeronetLonArr=[]

inputAeronetDataPath,outputAeronetDataPath=aeronetPath()

if dataLev == 'lev20':
        filePathArr=aotLib.getAeronetPathArr(inputAeronetDataPath + '/level20',dataLev)

else:
        dataLev = 'lev15'
        filePathArr=aotLib.getAeronetPathArr(inputAeronetDataPath + '/level15',dataLev)

nameStationArr,aeronetLatArr,aeronetLonArr=aotLib.returnAeronetCoordenateArr(filePathArr)

#print filePathArr
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
qFlagMat=[]
nameStationAux=[]
#--------------------------------------



#--------------------------------------
#

lenList, aotFileList=aotLib.getAotAquaFileList(filePath)
aotFileList = sorted(aotFileList)

#beginDay, endDay = extractLib.getMonthFirstAndLastDay(year,month)

beginDay =  getDay(year, month, day)

#print beginDay
endDay = beginDay

aotFileList = extractLib.getFileBetween2Days(beginDay, endDay, aotFileList)

#print aotFileList

for aotFilePath in aotFileList:

#	print aotFilePath
#	print(socket.gethostname())
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
			aotMean,aotStd,aotMatrix,latMatrix,lonMatrix,flagMatrix=aotProcess(filePath,aotFilePath,\
str(time),aeronetLatArr[nameStation],aeronetLonArr[nameStation])
			
				
			#print aotMean

			if aotMean >=0:
				nameStationAux=nameStationAux+[nameStationArr[nameStation]]
				aotArr40 = aotArr40 + [aotMatrix]
				latArr40 = latArr40 + [latMatrix]
				lonArr40 = lonArr40 + [lonMatrix]
				qFlagMat = qFlagMat + [flagMatrix]

			else:
				pass

		except:
#			print "I/O error({0}): {1}".format(e.errno, e.strerror)


#		except:
		#	print 'Error'
			pass

	gc.collect()
#--------------------------------------
	for station in range(len(nameStationAux)):


		tempFile = tempOutputPath+'/tempData_'+sensor+'_'+resolution+'_'+nameStationAux[station]+'_'+year+'_'+str(time)+'_aotArr40.p'
		pickle.dump(aotArr40[station], open(tempFile, 'wb'))

		tempFile = tempOutputPath+'/tempData_'+sensor+'_'+resolution+'_'+nameStationAux[station]+'_'+year+'_'+str(time)+'_latArr40.p'
		pickle.dump(latArr40[station], open(tempFile, 'wb'))

		tempFile = tempOutputPath+'/tempData_'+sensor+'_'+resolution+'_'+nameStationAux[station]+'_'+year+'_'+str(time)+'_lonArr40.p'
		pickle.dump(lonArr40[station], open(tempFile, 'wb'))

		tempFile = tempOutputPath+'/tempData_'+sensor+'_'+resolution+'_'+nameStationAux[station]+'_'+year+'_'+str(time)+'_qFlagMat.p'
		pickle.dump(qFlagMat[station], open(tempFile, 'wb'))
		#print tempFile

	timeArr=np.append(timeArr,time)

#--------------------------------------
# write data arrays in hdf5 file
#
#

#	try:

#	        aotLib.writeData(outputAquaDataPath,satellite + resolution,nameStationAux,year,time,aotArr40,latArr40,lonArr40)
#        	timeArr=np.append(timeArr,time)#remove this when to write in lib file

#		print(Fore.YELLOW + 'DATA WROTE')
#		print(Styele.RESET_ALL)


#	except:
#		print(Fore.RED + 'NO DATA TO WROTE')
#		print(Style.RESET_ALL)
	
#--------------------------------------
        aotArr40=[]
        latArr40=[]
        lonArr40=[]
	qFlagMat=[]
        nameStationAux=[]


tempFile = tempOutputPath+'/tempData_'+sensor+'_'+resolution+'_'+year+'_'+month+'_'+day+'_timeArr.p'
pickle.dump(timeArr, open(tempFile, 'wb'))

gc.collect()

#--------------------------------------
# write time array in hdf5 file
#
#

#try:

#	aotLib.writeDataTime(outputAquaDataPath,year,timeArr,satellite + resolution, processId)

#	print(Fore.YELLOW + 'TIME WROTE')
#	print(Styele.RESET_ALL)

#except:

#	print(Fore.RED + 'NO TIME TO WRITE')
#	print(Style.RESET_ALL)
#--------------------------------------

