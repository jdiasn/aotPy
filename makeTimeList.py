
import numpy as np
from aotConf import aotGridded
import h5py as h5
from sys import argv

h5DataPath = aotGridded()



##### creat time appended #####
dataSetPath = h5DataPath+'/'+'aotDataSet.h5'
aotDataSet = h5.File(dataSetPath)
year = argv[1]
satellite = argv[2]
resolution = argv[3]


timeSatelliteArr=np.array([])
allTimeSatelliteArr=np.array([])

#months=['01','02','03','04','05','06','07']
months=['01','02','03','04','05','06','07','08','09','10','11','12']

#months=['09']

for month in months:
    try:
        timeSatelliteArr=np.array(aotDataSet['/time/'+year+'/'+satellite+resolution+'/'+satellite+resolution+month])
	allTimeSatelliteArr=np.append(allTimeSatelliteArr,np.unique(timeSatelliteArr))

    except:
        print 'without '+'/time/'+year+'/'+satellite+resolution+'/'+satellite+resolution+month
       
    #allTimeSatelliteArr=np.append(allTimeSatelliteArr,np.unique(timeSatelliteArr))
    
try:
    del aotDataSet['time'+'/'+year+'/'+satellite+resolution+'/'+satellite+resolution]

except:
    print 'without timeSerie'

#print allTimeSatelliteArr

aotDataSet['time'+'/'+year+'/'+satellite+resolution+'/'+satellite+resolution]=allTimeSatelliteArr
aotDataSet.close()
