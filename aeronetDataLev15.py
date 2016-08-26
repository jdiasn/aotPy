
import numpy as np
import h5py as h5

from sys import argv
import mpi4py as MPI

import aotLib
from aotConf import aeronetPath
from aotConf import aotGridded

############ main code ############
aotAeroMean=np.array([])
aotAeroStd=np.array([])
aotAero550Mean=np.array([])
aotAero550Std=np.array([])
newTimeArr=np.array([])

inputAeronetDataPath, outputAeronetDataPath=aeronetPath()
pathOut=aotGridded()

year=argv[1]
satellite=argv[2]
resolution=argv[3]
dataLev = argv[4]

#comm = MPI.COMM_WORLD

#size = comm.Get_size()
#rank = comm.Get_rank()

dataPath=pathOut+'/'+'aotDataSet.h5'
aotData=h5.File(dataPath,'r')
timeSatelliteArr=np.array(aotData['/time/'+year+'/'+satellite+resolution+'/'+satellite+resolution])
aotData.close()
device='aeronet'

#get list of aeronet archive

if dataLev == 'lev20':
	filePathArr=aotLib.getAeronetPathArr(inputAeronetDataPath + '/level20',dataLev)


else:
	dataLev = 'lev15'
	filePathArr=aotLib.getAeronetPathArr(inputAeronetDataPath + '/level15',dataLev)


#print filePathArr

stationNameArr=aotLib.returnAeronetCoordenateArr(filePathArr)[0]

#print stationNameArr

for filePath in range(len(filePathArr)):

#	print filePathArr[filePath]
	table,aotWlenHeader=aotLib.getAeronetDataTable(filePathArr[filePath])	

	table = table[(table.Date_dd_mm_yy_.str.split(':').str[2] == year)]

		
	for timeSat in timeSatelliteArr:
		aot=table[(table.Julian_Day>timeSat-30/1440.)&(table.Julian_Day<timeSat+30/1440.)].AOT_500	
		aot=aot.dropna()		

		aot550Arr=np.array([])
		for line in aot.index:
			aot550=aotLib.getInterpolatedAot(table,aotWlenHeader,line)
			aot550Arr=np.append(aot550Arr,aot550)				

		if aot.mean()>=0:

			aotAero550Mean=np.append(aotAero550Mean,aot550Arr.mean())
			aotAero550Std=np.append(aotAero550Std,aot550Arr.std())
		   	aotAeroMean=np.append(aotAeroMean,aot.mean())
			aotAeroStd=np.append(aotAeroStd,aot.std())
			newTimeArr=np.append(newTimeArr,timeSat)



	aotLib.writeAeroData(pathOut,device,satellite + resolution,stationNameArr[filePath],year,newTimeArr,aotAeroMean,aotAeroStd,'500')
	aotLib.writeAeroData(pathOut,device,satellite + resolution,stationNameArr[filePath],year,newTimeArr,aotAero550Mean,aotAero550Std,'550')
	aotAeroMean=np.array([])
	aotAeroStd=np.array([])
	newTimeArr=np.array([])
	aotAero550Mean=np.array([])
	aotAero550Std=np.array([])


