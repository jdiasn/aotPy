#this file is used to set path to use at input and output data
from os import environ

homePath = environ['HOME']

dataPath = homePath + '/aotData'
inputDataPath = dataPath + '/inputData'
outputDataPath = dataPath + '/outputData'
outputTempDataPath = '/state/partition1' + '/outputData'


#------------------------------------------------------------
#
def aotGridded():
        
        griddedDataPath = dataPath + '/aotGridded'

        return griddedDataPath


#------------------------------------------------------------
#
def edrNppNasaPath():

	inputNppDataPath = inputDataPath + '/viirs/edr'
	outputNppDataPath = outputDataPath + '/viirs/edr'

	return inputNppDataPath, outputNppDataPath

def edrCsppPath():

	inputNppDataPath = inputDataPath + '/npp/edrCsppAsc'
	outputNppDataPath = outputDataPath +  '/npp/edrCsppAsc'

	return inputNppDataPath, outputNppDataPath


def ipNppNasaPath():

	inputNppDataPath = inputDataPath + '/viirs/ip'
	outputNppDataPath = outputDataPath + '/viirs/ip'

	return inputNppDataPath, outputNppDataPath


#------------------------------------------------------------
#
def aotModis3k():

        inputNppDataPath = inputDataPath + '/modis/3km' 
        outputNppDataPath = outputDataPath + '/modis/3km'

        return inputNppDataPath, outputNppDataPath

def aotModis():

        inputNppDataPath = inputDataPath + '/modis/10km' 
        outputNppDataPath = outputDataPath + '/modis/10km'

        return inputNppDataPath, outputNppDataPath


def aeronetPath():

	inputAeronetDataPath = inputDataPath + '/aeronet'
	outputAeronetDataPath = outputDataPath + '/aeronet'

	return inputAeronetDataPath, outputAeronetDataPath


