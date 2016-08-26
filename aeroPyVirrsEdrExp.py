import numpy as np
import h5py as h5
import pandas as pd

import gc
import pickle
from mpi4py import MPI
from sys import argv
from colorama import Fore, Back, Style

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


if sensor == 'viirs' and resolution == 'edr':

    from aotConf import edrNppNasaPath
    inputSatPath, outputSatPath = edrNppNasaPath()

else:

    from aotConf import ipNppNasaPath
    inputSatPath, outputSatPath = ipNppNasaPath()


def strRank(rank):

        if rank < 9:
                strRank = '0' + str(rank + 1)

        else:
                strRank = str(rank + 1)

        return strRank



def aotProcess(filePath,gaeroFile,vaoooFile,julianDay,aeronetLat,aeronetLon):

        date=vaoooFile[56:64]
        vaooo=h5.File(vaoooFile,'r')
	factors=np.array(vaooo['/All_Data/VIIRS-Aeros-EDR_All/AerosolOpticalDepthFactors'])
        aeroOptDep=np.array(vaooo['/All_Data/VIIRS-Aeros-EDR_All/AerosolOpticalDepth_at_550nm'])
        qualFlag1=np.array(vaooo['/All_Data/VIIRS-Aeros-EDR_All/QF1_VIIRSAEROEDR'])
        qualFlag4=np.array(vaooo['/All_Data/VIIRS-Aeros-EDR_All/QF4_VIIRSAEROEDR'])
        vaooo.close()
        del vaooo

        #--data cleaner-----------
        aeroOptDep10=aeroOptDep*factors[0]+factors[1]
        #-------------------------

        del aeroOptDep
        gc.collect()

        gaero=h5.File(gaeroFile,'r')
        lat=np.array(gaero['/All_Data/VIIRS-Aeros-EDR-GEO_All/Latitude'])
        lon=np.array(gaero['/All_Data/VIIRS-Aeros-EDR-GEO_All/Longitude'])
        gaero.close()

        del gaero
        gc.collect()

        #-----aeronet position--------
        #aeronet= -10.0,-54.5
        #aeronet=-15.729500,-56.021000
        earthRay= 6371 ## km
        length= 40 ## km

        beginLatReg,endLatReg,beginLonReg,endLonReg=aotLib.getComparisonRegion(aeronetLat,aeronetLon,length,earthRay)
        rowMin,rowMax,colMin,colMax=aotLib.getRegionIndexMatrix(beginLatReg,endLatReg,lat,beginLonReg,endLonReg,lon)
        qualFlag1=aotLib.getNewMatrix(rowMin,rowMax,colMin,colMax,qualFlag1)
        aeroOptDep10=aotLib.getNewMatrix(rowMin,rowMax,colMin,colMax,aeroOptDep10)
        lat=aotLib.getNewMatrix(rowMin,rowMax,colMin,colMax,lat)
        lon=aotLib.getNewMatrix(rowMin,rowMax,colMin,colMax,lon)	
	qualFlag4=aotLib.getNewMatrix(rowMin,rowMax,colMin,colMax,qualFlag4)

#       aeroOptDep10=aotLib.RemoveBadData2(qualFlag1,aeroOptDep10,'10','00')
        aeroOptDep10=aotLib.removeBadDataBitwise(qualFlag1,aeroOptDep10,3,3)

#        print aeroOptDep10.mean()

#       #--do aotLib.plot2----------------
#       #---coordenates around station
#
#       length=100 #len
#       coordenates=aotLib.getComparisonRegion(aeronetLat,aeronetLon,length,earthRay)
#
#       beginLatFig,endLatFig=coordenates[0],coordenates[1]
#       beginLonFig,endLonFig=coordenates[2],coordenates[3]
#       figName=(filePath+julianDay+'bit10')
#       title=('AOT em NPP bit 10 '+date)
#       aotLib.doPlot2(lon,lat,aeroOptDep10,title,figName,beginLatFig,endLatFig,beginLonFig,endLonFig)#,\
#       #beginLatReg,endLatReg,beginLonReg,endLonReg)

        gc.collect()
        return aeroOptDep10.mean(),aeroOptDep10.std(),aeroOptDep10,lat,lon,qualFlag4,qualFlag1
#--------------------------------------


####################################
# main code
#
#-----------------------------------

comm = 	MPI.COMM_WORLD

size = comm.Get_size()
rank = comm.Get_rank()

try:
	
	day = argv[7]

except:
	
	day = strRank(rank)


pathOut = '/'.join([outputSatPath, year])
filePath = '/'.join([inputSatPath, year])

#----------------------------------

#print filePath
#----------------------------------
# geometric paramenters
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

#print 'arr',inputAeronetDataPath
nameStationArr,aeronetLatArr,aeronetLonArr=aotLib.returnAeronetCoordenateArr(filePathArr)
#----------------------------------

#--------------------------------------
# array variables
#
lenList=[]
gaeroFileList=[]
vaoooFileList=[]
timeArr=np.array([])
aotMeanArr=np.array([])
aotMeanList=[]
aotStdArr=np.array([])
aotStdList=[]
aotArr40=[]
latArr40=[]
lonArr40=[]
aotModel=[]
qFlagMat=[]
nameStationAux=[]
#--------------------------------------

#--------------------------------------
# it is used to retrieve all available  
# data

lenList, vaoooFileList = aotLib.getEdrAotFileListNasa(filePath, year, month, day)
vaoooFileList = sorted(vaoooFileList)

#print lenList

for vaoooFile in vaoooFileList:
    
#        print vaoooFile

        fileName=vaoooFile.split('/')[-1]
        fildName=fileName.split('_')    

#        year=fildName[2][1:5]
#        month=fildName[2][5:7]
#        day=fildName[2][7:]
        hour=fildName[3][1:3]
        minute=fildName[3][3:5]
    
        julianDay=aotLib.getJulianDay(year,month,day) 
        decimalTime=aotLib.getDecimalTimeMinute(minute,hour)
        time=julianDay+round(decimalTime,5)
#        print 'time', time

#	print 'aqui'
#	print len(nameStationArr)
        for nameStation in range(len(nameStationArr)):  

#                print nameStationArr[nameStation]
                try: 
                        aotMean, aotStd, aotMatrix, latMatrix, lonMatrix, aotModelMatrix,flagMatrix = aotProcess(
				filePath, vaoooFile, vaoooFile, str(time), 
				aeronetLatArr[nameStation], aeronetLonArr[nameStation])


                        if aotMean >= 0:
                                nameStationAux = nameStationAux + [nameStationArr[nameStation]]
                                aotArr40 = aotArr40 + [aotMatrix]
                                latArr40 = latArr40 + [latMatrix]
                                lonArr40 = lonArr40 + [lonMatrix]
				aotModel = aotModel + [aotModelMatrix]
				qFlagMat = qFlagMat + [flagMatrix]


                #       print time,aotMean
                        else:
                                pass

                except:

                       # print 'Error'
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

		tempFile = tempOutputPath+'/tempData_'+sensor+'_'+resolution+'_'+nameStationAux[station]+'_'+year+'_'+str(time)+'_aotModel.p'
                pickle.dump(aotModel[station], open(tempFile, 'wb'))

		tempFile = tempOutputPath+'/tempData_'+sensor+'_'+resolution+'_'+nameStationAux[station]+'_'+year+'_'+str(time)+'_qFlagMat.p'
                pickle.dump(qFlagMat[station], open(tempFile, 'wb'))

		#print tempFile

        timeArr=np.append(timeArr,time)



#--------------------------------------
# write data in hdf5 file
#
#	try:
#        	aotLib.writeDataEdr(pathOut,satellite,nameStationAux,year,time,aotArr40,latArr40,lonArr40,aotModel,			qFlagMat)
 #       	timeArr=np.append(timeArr,time)

#		print(Fore.YELLOW + 'DATA WROTE')
#		print(Style.RESET_ALL)


#	except:
#		print(Fore.RED + 'NO DATA TO WRITE')
#		print(Style.RESET_ALL)
#--------------------------------------
        #aotMeanArr=aotMeanArr.reshape(len(timeArr),3)#numberStation)
        #print aotMeanArr
#       aotMeanList=aotMeanList+[aotMeanArr]
#       aotStdList=aotStdList+[aotStdArr]
        aotArr40=[]
        latArr40=[]
        lonArr40=[]
	aotModel=[]
        nameStationAux=[]    
	qFlagMat=[]

tempFile = tempOutputPath+'/tempData_'+sensor+'_'+resolution+'_'+year+'_'+month+'_'+day+'_timeArr.p'
pickle.dump(timeArr, open(tempFile, 'wb'))

gc.collect()




#print year

#try:
#	aotLib.writeDataTime(pathOut,year,timeArr,satellite,processId)	
	
#	print(Fore.YELLOW + 'TIME WROTE')
#	print(Style.RESET_ALL)

#except:
#	print(Fore.RED + 'NO TIME TO WRITE')
#	print(Style.RESET_ALL)

