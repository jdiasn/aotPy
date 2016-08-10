#!/usr/local/bin/python

import numpy as np
from aotConf import aeronetPath, nppPath
import h5py as h5
from sys import argv

inputAeronetDataPath,outputAeronetDataPath=aeronetPath()
outputNppDataPath=nppPath()[1]


##### creat time appended #####
nppPath=outputNppDataPath+'/'+'aotDataSet.h5'
nppData=h5.File(nppPath)
year=argv[1]
satellite=argv[2]


timeSatelliteArr=np.array([])
allTimeSatelliteArr=np.array([])

#months=['01','02','03','04','05','06','07']
months=['01','02','03','04','05','06','07','08','09','10','11','12']

#months=['09']

for month in months:
    try:
        timeSatelliteArr=np.array(nppData['/time/'+year+'/'+satellite+month])
	allTimeSatelliteArr=np.append(allTimeSatelliteArr,np.unique(timeSatelliteArr))

    except:
        print 'without '+'/time/'+year+'/'+satellite+month
       
    #allTimeSatelliteArr=np.append(allTimeSatelliteArr,np.unique(timeSatelliteArr))
    
try:
    del nppData['time'+'/'+year+'/'+satellite]
except:
    print 'without timeSerie'

nppData['time'+'/'+year+'/'+satellite]=allTimeSatelliteArr
nppData.close()
