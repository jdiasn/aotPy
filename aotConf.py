#this file is used to set path to use at input and output data
from os import environ

homePath = environ['HOME']

dataPath = homePath + '/aotData'
inputDataPath = dataPath + '/inputData'
outputDataPath = dataPath + '/outputData'
#outputDataPath = '/state/partition1' + '/outputData'


#------------------------------------------------------------
#
def aotGridded():
        
        griddedDataPath = dataPath + '/aotGridded'

        return griddedDataPath


#------------------------------------------------------------
#
def edrNppNasaPath():

	inputNppDataPath = inputDataPath + '/npp/edrDataNasa'
	outputNppDataPath = outputDataPath + '/npp/edrDataNasa'

	return inputNppDataPath, outputNppDataPath

def edrCsppPath():

	inputNppDataPath = inputDataPath + '/npp/edrCsppAsc'
	outputNppDataPath = outputDataPath +  '/npp/edrCsppAsc'

	return inputNppDataPath, outputNppDataPath


#------------------------------------------------------------
#
def aotModis3k():

        inputNppDataPath = inputDataPath + '/modis/3km' 
        outputNppDataPath = outputDataPath + '/modis/3km'

        return inputNppDataPath, outputNppDataPath

def aeronetPath():

	inputAeronetDataPath = inputDataPath + '/aeronet'
	outputAeronetDataPath = outputDataPat + '/aeronet'

	return inputAeronetDataPath, outputAeronetDataPath


