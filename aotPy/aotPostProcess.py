import numpy as np
import h5py as h5

def writeGriddedData(pathOut, satellite, sensor, year, varName, aotGridded):

	print  varName, pathOut

	aotOut = h5.File(pathOut)

	try: 
		del aotOut[satellite + '/' + sensor + '/' + str(year) + '/' + str(varName)]
			
	except:
		print 'without ' +satellite + '/' + sensor + '/' + str(year) + '/' + str(varName)

	aotOut[satellite + '/' + sensor + '/' + str(year) + '/' + str(varName)] = aotGridded

	aotOut.close()



