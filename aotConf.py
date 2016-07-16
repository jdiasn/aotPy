#!/usr/local/bin/python


#this file is used to set path to use at input and output data

inputDataPath='/Users/josedias/Documents/aotData'
outputDataPath='/Users/josedias/Documents/aotOutData'

def nppPath():

	inputNppDataPath=inputDataPath+'/npp'
	outputNppDataPath=outputDataPath
	return inputNppDataPath, outputNppDataPath

def edrNppPath():

	inputNppDataPath=inputDataPath+'/npp/edr'
	outputNppDataPath=outputDataPath
	return inputNppDataPath, outputNppDataPath

def edrNppPathNasa():

	inputNppDataPath=inputDataPath+'/npp/edrNasaAsc'
	outputNppDataPath=outputDataPath
	return inputNppDataPath, outputNppDataPath

def edrCsppPath():

	inputNppDataPath=inputDataPath+'/npp/edrCsppAsc'
	outputNppDataPath=outputDataPath
	return inputNppDataPath, outputNppDataPath

def aeronetPath():

	inputAeronetDataPath=inputDataPath+'/aeronet'
	outputAeronetDataPath=outputDataPath
	return inputAeronetDataPath, outputAeronetDataPath


def aquaPath():

	inputAquaDataPath=inputDataPath+'/aqua'
	outputAquaDataPath=outputDataPath
	return inputAquaDataPath, outputAquaDataPath


