import pickle
import glob
import numpy as np

import aotLib
from aotConf import aotGridded
from sys import argv

year = argv[1]
month = argv[2]
satellite = argv[3]
sensor = argv[4]
resolution = argv[5]

allTimeSatelliteArr=np.array([])

if sensor == 'modis' and resolution == '3km':

    from aotConf import aotModis3k
    inputPath, outPutPath = aotModis3k()

elif sensor == 'modis' and resolution == '10km':

    from aotConf import aotModis
    inputPath, outPutPath = aotModis()

elif sensor == 'modis' and resolution == '10kmC51':

    from aotConf import aotModis
    inputPath, outPutPath = aotModisC51()

elif sensor == 'viirs' and resolution == 'edr':

    from aotConf import edrNppNasaPath
    inputPath, outPutPath = edrNppNasaPath()

else:
    print 'Configuration not found'


satelliteFilesPath = outPutPath + '/' + year

filesPathList = glob.glob(satelliteFilesPath + '/tempData*aotArr40.p')
filesPathList = sorted(filesPathList)

timeFilePath = glob.glob(satelliteFilesPath + '/tempData_*'+year+'_'+month+'*timeArr.p')
#print timeFilePath
griddedDataPath = aotGridded()

	

for filePath in filesPathList:

    #print filePath    
    path = filePath.split('/')[0:-1]
    path = '/'.join(path)
    
    variables = filePath.split('/')[-1].split('_') 
    
    time = variables[-2]
    nameStation = '_'.join(variables[3:-3])
    
    #print nameStation
    
   
    #print filePath
    #print path+'/'+latPath
    #print path+'/'+lonPath
    

    if sensor == 'modis':

        latPath = '_'.join(variables[0:-1])+'_'+'latArr40.p'
        lonPath = '_'.join(variables[0:-1])+'_'+'lonArr40.p'
	flgPath = '_'.join(variables[0:-1])+'_'+'qFlagMat.p'
 
   	aotArr40 = pickle.load(open(filePath, 'rb'))
	latArr40 = pickle.load(open(path+'/'+latPath, 'rb'))
    	lonArr40 = pickle.load(open(path+'/'+lonPath, 'rb'))
	qFlagMat = pickle.load(open(path+'/'+flgPath, 'rb'))
       
    	aotLib.writeData(griddedDataPath, satellite + resolution, nameStation,
			 year, time, aotArr40, latArr40, lonArr40, qFlagMat)

    if sensor == 'viirs':

        latPath = '_'.join(variables[0:-1])+'_'+'latArr40.p'
        lonPath = '_'.join(variables[0:-1])+'_'+'lonArr40.p'
        modPath = '_'.join(variables[0:-1])+'_'+'aotModel.p'
        flgPath = '_'.join(variables[0:-1])+'_'+'qFlagMat.p'

   	aotArr40 = pickle.load(open(filePath, 'rb'))
	latArr40 = pickle.load(open(path+'/'+latPath, 'rb'))
    	lonArr40 = pickle.load(open(path+'/'+lonPath, 'rb'))
	aotModel = pickle.load(open(path+'/'+modPath, 'rb'))
    	qFlagMat = pickle.load(open(path+'/'+flgPath, 'rb'))

        aotLib.writeDataEdr(griddedDataPath, satellite + resolution, nameStation,
			    year, time, aotArr40, latArr40, lonArr40, aotModel,
			    qFlagMat)
       
for filePath in timeFilePath:

	timeArr = pickle.load(open(filePath, 'rb'))
	allTimeSatelliteArr = np.append(allTimeSatelliteArr,np.unique(timeArr))
	
	allTimeSatelliteArr= np.sort(allTimeSatelliteArr) 

aotLib.writeDataTime(griddedDataPath, year, allTimeSatelliteArr, satellite+resolution,month)












#--------------------------------------
# write data arrays in hdf5 file
#
#

#       try:

#               aotLib.writeData(outputAquaDataPath,satellite + resolution,nameStationAux,year,time,aotArr40,latArr40,lonArr40)
#               timeArr=np.append(timeArr,time)#remove this when to write in lib file

#               print(Fore.YELLOW + 'DATA WROTE')
#               print(Styele.RESET_ALL)


#       except:
#               print(Fore.RED + 'NO DATA TO WROTE')
#               print(Style.RESET_ALL)

#--------------------------------------

#--------------------------------------
# write time array in hdf5 file
#
#

#try:

#       aotLib.writeDataTime(outputAquaDataPath,year,timeArr,satellite + resolution, processId)

#       print(Fore.YELLOW + 'TIME WROTE')
#       print(Styele.RESET_ALL)

#except:

#       print(Fore.RED + 'NO TIME TO WRITE')
#       print(Style.RESET_ALL)
#--------------------------------------

