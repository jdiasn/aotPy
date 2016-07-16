#!/usr/local/bin/python

import numpy as np
import h5py as h5
import gc
import aotLib
from colorama import Fore, Back, Style
#from aotConf import edrNppPath
from aotConf import aeronetPath
from sys import argv

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

        print aeroOptDep10.mean()

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
# edr work path
#
yearMonth=argv[1]

#satellite='edrNpp'
satellite='edrNppNasa'

if satellite == 'edrNppNasa':
	from aotConf import edrNppPathNasa
	inputNppDataPath,outputNppDataPath=edrNppPathNasa()

else:
	from aotConf import edrNppPath
	inputNppDataPath,outputNppDataPath=edrNppPath()

filePath=inputNppDataPath+'/'+yearMonth+'/'
pathOut=outputNppDataPath


processId=argv[2]
#----------------------------------

print filePath
#----------------------------------
# geometric paramenters
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
if satellite == 'edrNppNasa':
	lenList,gaeroFileList,vaoooFileList=aotLib.getEdrAotFileListNasa(filePath)
#	print 'here'

else:
	lenList,gaeroFileList,vaoooFileList=aotLib.getEdrAotFileList(filePath)

print lenList

for i in range(lenList):
    
        print vaoooFileList[i]

        fileName=vaoooFileList[i].split('/')[-1]
        fildName=fileName.split('_')    

        year=fildName[2][1:5]
        month=fildName[2][5:7]
        day=fildName[2][7:]
        hour=fildName[3][1:3]
        minute=fildName[3][3:5]
    
        julianDay=aotLib.getJulianDay(year,month,day) 
        decimalTime=aotLib.getDecimalTimeMinute(minute,hour)
        time=julianDay+round(decimalTime,5)
#        print 'time', time

        for nameStation in range(len(nameStationArr)):  
#        for nameStation in range(13,14):  


#                print nameStationArr[nameStation]
                try: 
                        aotMean, aotStd, aotMatrix, latMatrix, lonMatrix, aotModelMatrix,flagMatrix = aotProcess(
				filePath, gaeroFileList[i], vaoooFileList[i], str(time), 
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

                        print 'Error'
                       # pass
#--------------------------------------
#	print year

#--------------------------------------
# write data in hdf5 file
#
	try:
        	aotLib.writeDataEdr(pathOut,satellite,nameStationAux,year,time,aotArr40,latArr40,lonArr40,aotModel,			qFlagMat)
        	timeArr=np.append(timeArr,time)

		print(Fore.YELLOW + 'DATA WROTE')
		print(Style.RESET_ALL)


	except:
		print(Fore.RED + 'NO DATA TO WRITE')
		print(Style.RESET_ALL)
#--------------------------------------
        #aotMeanArr=aotMeanArr.reshape(len(timeArr),3)#numberStation)
        #print aotMeanArr
#       aotMeanList=aotMeanList+[aotMeanArr]
#       aotStdList=aotStdList+[aotStdArr]
        aotArr40=[]
        latArr40=[]
        lonArr40=[]
        nameStationAux=[]    
	qFlagMat=[]

#print year

try:
	aotLib.writeDataTime(pathOut,year,timeArr,satellite,processId)	
	
	print(Fore.YELLOW + 'TIME WROTE')
	print(Style.RESET_ALL)

except:
	print(Fore.RED + 'NO TIME TO WRITE')
	print(Style.RESET_ALL)

