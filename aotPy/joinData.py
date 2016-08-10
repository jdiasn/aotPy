import pickle
import glob
import numpy as np

from sys import argv

import aotPostProcess
from aotConf import aotGridded

year = argv[1]
satellite = argv[2]
sensor = argv[3]
resolution = argv[4]

griddedDataPath = aotGridded()

if sensor == 'modis' and int(resolution) == 3:
    
    from aotConf import aotModis3k
    inputPath, outPutPath = aotModis3k()
     
elif sensor == 'modis' and int(resolution) == 10:
    
    from aotConf import aotModis3k
    inputPath, outPutPath = aotModis3k()

elif sensor == 'viirs' and int(resolution) == 6:
    
    from aotConf import aotModis3k
    inputPath, outPutPath = aotModis3k()

else: 
    print 'Configuration not found'


beginLatReg, endLatReg = -60., 20.
beginLonReg, endLonReg = -96., -13.

lonGrid = np.arange(endLonReg, beginLonReg, -float(resolution)/111.2)
latGrid = np.arange(beginLatReg, endLatReg, float(resolution)/111.2)

xx, yy = np.meshgrid( lonGrid, latGrid)

satelliteFilesPath = outPutPath + '/' + year

outPutFileName = griddedDataPath + '/aotGriddedDataSet.h5'

filesPathList = glob.glob(satelliteFilesPath + '/aotMean*.p')
filesPathList = sorted(filesPathList)

for filePath in filesPathList:
    
    stepMonth = filePath.split('/')[-1].split('.')[0][-2:]
    aotMean = pickle.load(open(filePath, 'rb'))
    
    aotPostProcess.writeGriddedData(outPutFileName, satellite, sensor + resolution + 'km', year, stepMonth, aotMean)


filesPathList = glob.glob(satelliteFilesPath + '/aotFlag*.p')
filesPathList = sorted(filesPathList)

for filePath in filesPathList:
    
    stepMonth = filePath.split('/')[-1].split('.')[0][-2:]
    aotFlag = pickle.load(open(filePath, 'rb'))
    
    aotPostProcess.writeGriddedData(outPutFileName, satellite, sensor + resolution + 'km', year, stepMonth + 'flag',\
				     aotFlag)


aotPostProcess.writeGriddedData(outPutFileName, satellite, sensor + resolution + 'km', year, 'lon', xx)
aotPostProcess.writeGriddedData(outPutFileName, satellite, sensor + resolution + 'km', year, 'lat', yy)
