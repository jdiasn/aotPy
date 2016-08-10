import numpy as np
import matplotlib.pyplot as plt
import datetime
import math
from pandas import Series, DataFrame
from matplotlib.patches import Polygon
from mpl_toolkits.basemap import Basemap
from scipy.optimize import curve_fit
import glob
import pandas as pd
import h5py as h5


#################### SATELLITE #####################


#------------------------------------------
#A is quality flag matrix, B is AOT matrix, binNumber is bit group
#flag 
def RemoveBadData(A,B,binNumber):
	
    intNumber=np.uint8(binNumber)

    indexBadData=np.argwhere(A!=intNumber)    

    for i in indexBadData:
        B[i[0],i[1]]=-1.
    B = np.ma.masked_where(B<0,B)
    #np.ma.set_fill_value(B,np.nan)
    return B
#------------------------------------------


#------------------------------------------
#'A' is quality flag matrix. 'B' is AOT matrix. 'bit' is pair of
# numbers that cam be 76, 54, 32 e 10. 'valBit' is value associated
# to 'bit'
def RemoveBadData2(A,B,bit,valBit):
    #varBit=str(78-bit)
    varBit0,varBit1=7-int(bit[0]),8-int(bit[1])
    badMatrixData=[]
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            binNumber='{0:08b}'.format(A[i,j],2)
            
            bit76=binNumber[0:2]
            bit54=binNumber[2:4]
            bit32=binNumber[4:6]
            bit10=binNumber[6:8]
            
            #if binNumber[varBit0:varBit1]==valBit:
             #   print binNumber+' bit10: '+str(bit10)+' bit32: '+str(bit32)+' bit54: '+str(bit54)+' bit76: '+str(bit76)+' dado bom'

            if binNumber[varBit0:varBit1]!=valBit:
                badMatrixData+=[[i,j]]
             #   print binNumber+' bit10: '+str(bit10)+' bit32: '+str(bit32)+' bit54: '+str(bit54)+' bit76: '+str(bit76)
                
    badMatrixData=np.array(badMatrixData)
    for i in badMatrixData:
        B[i[0],i[1]]=-1.
    B = np.ma.masked_where(B<0,B)
    print 'end bit '+bit
    return B


def removeBadDataBitwise(A,B,maskBit,valBit):

#	for index in np.argwhere(A & 3 !=0):
#		B[index[0],index[1]]=-1
#	B = np.ma.masked_where(A & maskBit !=valBit,B)
	
	#print 'end bit'
#	return B
	return np.ma.masked_where(A & maskBit !=valBit,B)
#	return np.ma.masked_array(B,A & maskBit != valBit)


#------------------------------------------


#------------------------------------------
# this function return a index list for values between two values 
# ('begin' and 'end') in 2d array

def getValBetAt2dArr(begin,end,Arr):
    
    indexBegin=np.argwhere(Arr>=begin)
    indexEnd=np.argwhere(Arr<=end)
    listBegin=[]
    listEnd=[]
    
    for i in indexBegin:
        listBegin+=[str(i[0])+','+str(i[1])]
	#print Arr[i[0],i[1]]
        #print latListBegin
    for i in indexEnd:
        listEnd+=[str(i[0])+','+str(i[1])]
   
    #print listBegin,listEnd	 
    interBeginEnd=np.intersect1d(listBegin,listEnd)

   # print interBeginEnd
    return interBeginEnd
#------------------------------------------


#------------------------------------------
# this function return a index list for values between two values 
# ('begin' and 'end') in 2d array

def getValBetAt2dArrB(rowMina,colMina,begin,end,Arr):
    
    indexBegin=np.argwhere(Arr>=begin)
    indexEnd=np.argwhere(Arr<=end)
    listBegin=[]
    listEnd=[]
    
    for i in indexBegin:
        listBegin+=[str(i[0]+rowMina)+','+str(i[1]+colMina)]
	#print Arr[i[0],i[1]]
        #print latListBegin
    for i in indexEnd:
        listEnd+=[str(i[0]+rowMina)+','+str(i[1]+colMina)]
   
    #print listBegin,listEnd	 
    interBeginEnd=np.intersect1d(listBegin,listEnd)

   # print interBeginEnd
    return interBeginEnd
#------------------------------------------


#------------------------------------------
#this function creat a color screen over an area
#
def drawScreen(beginLat,endLat,beginLon,endLon,m):
    lats = [endLat,beginLat,beginLat,endLat]#beginLat,endLat,endLat,beginLat
    lons = [endLon,endLon,beginLon,beginLon]#beginLon,beginLon,endLon,endLon
    x, y = m( lons, lats )
    xy = zip(x,y)
    poly = Polygon( xy, facecolor='red', alpha=0.5 )
    plt.gca().add_patch(poly)
#-----------------------------------------


#-----------------------------------------
#this function do average in 2d array using index list
#variables 'lat' and 'lon' are array
def regionAverage(latBegin,latEnd,lat,lonBegin,lonEnd,lon,A):
    sumation=np.array([])
    #print A
    #value=np.array([])
#get intersection between two 2d array (lat and lon)
    interLatBeginEnd=getValBetAt2dArr(latBegin,latEnd,lat)
    interLonBeginEnd=getValBetAt2dArr(lonBegin,lonEnd,lon)
    interLatLon=np.intersect1d(interLatBeginEnd,interLonBeginEnd)
    #print interLatLon
#----do average of values
    for i in interLatLon:
	 i0,i2=i.split(',')
         sumation=np.append(sumation,A[i0,i2])
	 value=np.sort(sumation)
    #print 'size', sumation.size
    #print value
    #print sumation	
    average=np.mean(sumation)
    #print sumAot, len(interLatLon), averageAot
    return average,value#,interLatLon

#-----------------------------------------


#-----------------------------------------
#
#
def getNewMatrix(rowMin,rowMax,colMin,colMax,matrix):
    
    matrix=matrix[rowMin:rowMax+1,colMin:colMax+1]
    
    return matrix
#-----------------------------------------


#-----------------------------------------
#
#
def getMatrixCorner(arrayIntersec):
    
    row=np.array([])
    col=np.array([])

    #row=[]
    #col=[]		

    for i in arrayIntersec:
        i0,i1=i.split(',')
        row=np.append(row,int(i0))
        col=np.append(col,int(i1))
	#row=row+[i0]
	#col=col+[i1]
    
    #row=np.array(row,dtype='int')
    #col=np.array(col,dtype='int')
   
    row=np.sort(row)	
    col=np.sort(col)

    return int(row[0]),int(row[-1]),int(col[0]),int(col[-1])

    #return row.min(),row.max(),col.min(),col.max()
#-----------------------------------------


#-----------------------------------------
#
#
def getRegionIndexMatrixOld(latBegin,latEnd,lat,lonBegin,lonEnd,lon):

	try:
    		interLatBeginEnd=getValBetAt2dArr(latBegin,latEnd,lat)
    		#print interLatBeginEnd
	except:
		print 'out of latitude'
		
    	rowMina,rowMaxa,colMina,colMaxa=getMatrixCorner(interLatBeginEnd)

	if(lonBegin>=lon[rowMaxa][colMaxa] and lonEnd<=lon[rowMina][colMina]):

	    	lon=getNewMatrix(rowMina,rowMaxa,colMina,colMaxa,lon)

		try:
    			interLonBeginEnd=getValBetAt2dArrB(rowMina,colMina,lonBegin,lonEnd,lon)
    			#print interLonBeginEnd
		   	interLatLon=np.intersect1d(interLatBeginEnd,interLonBeginEnd)

		except:
			print 'out of longitude'
			
 		try: 
		  	rowMin,rowMax,colMin,colMax=getMatrixCorner(interLatLon)

		except:
			print 'without longitude values'
		
	else:
		print 'out of longitude 2'
	
	try: 		
    		return rowMin,rowMax,colMin,colMax
	
	except:
		print 'no values'
#-----------------------------------------


#-----------------------------------------
#
#
def getRegionIndexMatrix(latBegin,latEnd,lat,lonBegin,lonEnd,lon):

	try:

		ind=((lat>=latBegin) & (lat<=latEnd) & (lon>=lonBegin) & (lon<=lonEnd))
		ind=np.argwhere(ind==True)

		rowMax=ind[:,0].max()
		rowMin=ind[:,0].min()

		colMax=ind[:,1].max()
		colMin=ind[:,1].min()
		
		#ind=ind.transpose()
		#rowMax=ind[0].max()
		#rowMin=ind[0].min()

		#colMax=ind[1].max()
		#colMin=ind[1].min()

	except:
		print 'out of lat lon'
		return None
	
	return rowMin,rowMax,colMin,colMax

#-----------------------------------------


#-----------------------------------------
def getJulianDay(strYear,strMonth,strDay):

#        strDay=line[9:11]
#        strMonth=line[6:8]
#        strYear=line[1:5]
        strTime=strYear+" "+strMonth+" "+strDay
        julianDay=datetime.datetime.strptime(strTime, '%Y %m %d').strftime('%j')
        #print strDay, strMonth, strYear, julianDay
	#print julianDay
        return float(julianDay)
#-----------------------------------------



#-----------------------------------------
#
#
def getDecimalTimeMinute(minute,hour):

        decimalMinute=float(minute)/60.0**2
        decimalTime=float(hour)/24.0+decimalMinute
                        
	#print hourNumber, minuteNumber, decimalMinute, decimalTime     
        return(decimalTime)
#-----------------------------------------


#-----------------------------------------
#this function get a list of npp files to 
#plot aot npp
#
def getAotFileList(filePath):
 
#    print filePath
    pathIvaotList=[]
    pathGmtcoList=[]
    pathIvaot=filePath+'IVAOT*.h5'
    pathList=glob.glob(pathIvaot)
    for ivaotFile in pathList:

        dateTime=ivaotFile[55:82]
        pathGmtco=glob.glob(filePath+'GMTCO*'+dateTime+'*.h5')
    
        if len(pathGmtco)<2:
        #print dateTime, len(d)
        #print ivaotFile
        #print pathGmtco[0]

#		if len(pathGmtco)<1:
#			break
 		try:       
        		pathGmtcoList.append(pathGmtco[0])
        		pathIvaotList.append(ivaotFile)

		except:
			pass

#    print pathGmtcoList
    return len(pathGmtcoList),pathGmtcoList,pathIvaotList
#-----------------------------------------


#-----------------------------------------
#this function remove zero values from AOT
#array

def removeZeroValues(arr):
	index=np.argwhere(arr==0.)
	arr=np.delete(arr,index)
	return arr

#-----------------------------------------



#-----------------------------------------
#Function to get cordenates using Aeronte 
#lat and long reference

def getComparisonRegion(lat,lon,length,ray):

	beginLatReg=lat-length*180/(2.*ray*math.pi)
	endLatReg=lat+length*180/(2.*ray*math.pi)
	beginLonReg=lon-length*180/(2.*ray*math.pi)
	endLonReg=lon+length*180/(2.*ray*math.pi)

	return beginLatReg,endLatReg,beginLonReg,endLonReg
#-----------------------------------------


#-----------------------------------------
#This function do a plot of AOT data
#
def doPlotHistogram(valueArr):

	plt.hist(valueArr,12,normed=1,facecolor='green',alpha=0.5)
	plt.show()


#-----------------------------------------


#-----------------------------------------
#This function do a plot of AOT data
#
def doPlot2(lon,lat,aeroOptDep,title,figName,beginLatFig=-60,endLatFig=20,beginLonFig=-96,endLonFig=-13,\
beginLatReg=0,endLatReg=0,beginLonReg=0,endLonReg=0):

	m=Basemap(projection='cyl',resolution='l',llcrnrlat=beginLatFig,\
urcrnrlat=endLatFig,llcrnrlon=beginLonFig,urcrnrlon=endLonFig)
	#lon,lat=m(lon,lat)

	print figName
	parallels = np.arange(beginLatFig,endLatFig,(endLatFig-beginLatFig)/8.)
	m.drawparallels(parallels,labels=[1,0,0,1])
	meridians = np.arange(beginLonFig,endLonFig,(endLonFig-beginLonFig)/4.)
	m.drawmeridians(meridians,labels=[1,0,0,1])
        m.drawcountries(linewidth=0.5)
        m.drawcoastlines(linewidth=0.5)
        m.pcolormesh(lon,lat,aeroOptDep,vmin=0.,vmax=1)
	if beginLatReg==0 and endLatReg==0 and beginLonReg==0 and\
endLonReg==0:
		pass

	else:	
	       	drawScreen(beginLatReg,endLatReg,beginLonReg,endLonReg,m)
		#print beginLatReg,endLatReg,beginLonReg,endLonReg
        cb=m.colorbar()
        plt.title(title)
        plt.savefig(figName+'.png',format='png',dpi=150)
        plt.clf()
       #plt.show()
#-------------------------

##################### MODIS #########################


def getAotAquaFileList(filePath):

        aerosolList=[]

	try:
	        pathAerosol=filePath+'AEROSOL*.h5'

	except:
		print('Without AEROSOL*.h5\n')
		print('Searching for MYD04*.h5')

	try:
		
	        pathAerosol=filePath+'MYD04*.h5'
	except:
		print('Wthiout AOT files')

        pathList=glob.glob(pathAerosol)

        return len(pathList), pathList

def removeValues(arg,lat,lon,aot):
    inter=np.argwhere(lat==arg)  
    line=np.array([],dtype=int)  
         
    for i in inter:
        line=np.append(line,i[0])  
                
    line=np.unique(line)  
         
    if line.size == 0:  
        parameter=0
        #print 'empty'
             
    elif line.size == 1:                   
        if line[0]<lat.shape[0]-line[0]:  
            lat=lat[line[0]+1:]
            lon=lon[line[0]+1:]  
            aot=aot[line[0]+1:]  
            #print '1'  
            parameter=1  
                 
        else:  
            lat=lat[:line[0]] 
            lon=lon[:line[0]]
            aot=aot[:line[0]]
            #print '2'  
            parameter=1

    else:
        if line[-1]-line[0]<lat.shape[0]/2 and line[-1]+line[0]/2 < lat.shape[0]/2:
            lat=lat[line[-1]+1:]
            lon=lon[line[-1]+1:]
            aot=aot[line[-1]+1:]
            #print '3'  
            parameter=1

        elif line[-1]-line[0]<lat.shape[0]/2 and line[-1]+line[0]/2 > lat.shape[0]/2:
            lat=lat[:line[-1]]
            lon=lon[:line[-1]]
            aot=aot[:line[-1]]
            #print '4'  
            parameter=1

        else:
            lat=lat[line[0]+1:line[-1]]
            lon=lon[line[0]+1:line[-1]]
            aot=aot[line[0]+1:line[-1]]
            #print '5'  
            parameter=1

    return lat,lon,aot,parameter








#################### AERONET ########################

#------------------------------------------
#this funtion get aeronet Dic file
#
def getAeronetDirectoryFile(aeronetPathDir):

    try:    
        aeronetFile=aeronetPathDir.split('/')[-1].split('.')[0]
        #print aeronetPathList[0]
        date=aeronetFile[0:14]
        stationName=aeronetFile[14:]
        #print stationName, date
        return stationName, date
    
    except:
        print 'was not possible to open'
#------------------------------------------


#------------------------------------------
#this funcition get aeronet coordenate from
#.lev15 data table
def getAeronetCoordenates(dataTable):
        geome=(dataTable.loc[[0],:])[0][0]
        geome=geome.split(',')
        station=geome[0].split('=')[1];# print station
        lon=float(geome[1].split('=')[1]);# print lon
        lat=float(geome[2].split('=')[1]);# print lat

        return station, lat, lon
#------------------------------------------


def getAeronetPathArr(inputAeronetDataPath, dataLev):

        filePathArr=[]  

        aeronetPathList=glob.glob(inputAeronetDataPath+'/*.'+dataLev)

        for dirStation in aeronetPathList:
                stationName,date=getAeronetDirectoryFile(dirStation)
                filePath=inputAeronetDataPath+'/'+date+stationName+'.'+dataLev
                filePathArr.append(filePath)

        return filePathArr

def returnAeronetCoordenateArr(filePathArr):

        stationNameArr=[]
        latArr=[]
        lonArr=[]

        for aeronetFilePath in filePathArr:
                dataTable=pd.read_table(aeronetFilePath,skiprows=2,header=None)
                stationName,lat,lon=getAeronetCoordenates(dataTable)
		if '_' in stationName:
			stationName=stationName.replace('_','_')
		if '-' in stationName:
			stationName=stationName.replace('-','_')
                stationNameArr.append(stationName)
                latArr.append(lat)
                lonArr.append(lon)

        return stationNameArr, latArr, lonArr


def getAeronetDataTable(filePath):

        table=pd.read_table(filePath,skiprows=4,header=None)
        headerN=(table.loc[[0],:])[0][0]
        headerN=headerN.replace('-','_').replace('(','_').replace(')','_').replace('/','_').replace('[','_').replace(']','_').replace(':','_')
        headerN=headerN.split(',')
        table=pd.read_table(filePath,skiprows=5,sep=',',header=None,names=headerN)
    
        return table,headerN[3:19]

def writeAeroData(pathOut,device,satellite,nameStation,year,time,aotAeroMean,aotAeroStd,wLen):

        aotOut=h5.File(pathOut+'/'+'aotDataSet.h5')

        try:
                del aotOut[device+'/'+satellite+'/'+nameStation+'/'+year+'/aotMean/aotMean'+wLen]
        except:
                print 'without '+nameStation+' aotMean'

        try:
                del aotOut[device+'/'+satellite+'/'+nameStation+'/'+year+'/aotStd/aotStd'+wLen]
        except:
                print 'without '+nameStation+' aotStd'

        try:
                del aotOut[device+'/'+satellite+'/'+nameStation+'/'+year+'/aotTime/aotTime'+wLen]
        except:
                print 'without '+nameStation+' time'

        aotOut[device+'/'+satellite+'/'+nameStation+'/'+year+'/aotMean/aotMean'+wLen]=aotAeroMean
        aotOut[device+'/'+satellite+'/'+nameStation+'/'+year+'/aotStd/aotStd'+wLen]=aotAeroStd
        aotOut[device+'/'+satellite+'/'+nameStation+'/'+year+'/aotTime/aotTime'+wLen]=time

        aotOut.close()

def fitFunc2(lam,a,b,c,d):
    return (a/lam)+b**(c*lam)+d


def getInterpolatedAot(table,aotLenHeader,line):
        aotValueArr=np.array([])
        waveLenList=[]
        waveLenArr=([])
        for aotWlen in aotLenHeader:
            #print aotWlen
            aotValue=np.array(DataFrame(table,columns=[aotWlen]).loc[[line]])
            if aotValue>=0:
                aotValueArr=np.append(aotValueArr,aotValue)
                waveLen=aotWlen.split('_')[1]
                waveLenList.append(waveLen)
                waveLenArr=np.array(waveLenList,dtype='float64')

        fitParams, fitCovariances = curve_fit(fitFunc2, waveLenArr, aotValueArr)
        aot550=fitFunc2(550, fitParams[0], fitParams[1],fitParams[2],fitParams[3])
        return aot550 

##################### edrViirs data ###########################

#-----------------------------------------
#this function get a list of npp edr files to 
#plot aot edr npp
#
def getEdrAotFileList(filePath):

    pathVaoooList=[]
    pathGaeroList=[]
    pathVaooo=filePath+'VAOOO*.h5'
    pathList=glob.glob(pathVaooo)
   
    for vaoooFile in pathList:

        dateTime=vaoooFile[54:]
        pathGaero=glob.glob(filePath+'GAERO*'+dateTime)

        if len(pathGaero)<2:

                try:
                        pathGaeroList.append(pathGaero[0])
                        pathVaoooList.append(vaoooFile)

                except:
                        pass
    
    return len(pathGaeroList),pathGaeroList,pathVaoooList
#-----------------------------------------


#-----------------------------------------
#this function get a list of npp edr files to 
#plot aot edr npp from nasa
#
def getEdrAotFileListNasa(filePath):

    pathGaeroList=[]
    pathGaero=filePath+'GAERO*.h5'
    pathGaeroList=glob.glob(pathGaero) 
       
    return len(pathGaeroList),pathGaeroList,pathGaeroList
#-----------------------------------------


#-----------------------------------------
#
#
#
def writeDataEdr(pathOut,satellite,nameStation,year,time,aotArr40,latArr40,lonArr40,aotModel,qFlagMat):

        aotOut=h5.File(pathOut+'/'+'aotDataSet.h5')

        for i in range(len(nameStation)):

                try:
                        del aotOut[satellite+'/'+nameStation[i]+'/'+year+'/aot40x40/'+str(time)+'aot40x40']
                except:
                        print 'without '+nameStation[i]+' '+str(time)+'aot40x40'

                try:
                        del aotOut[satellite+'/'+nameStation[i]+'/'+year+'/lat40x40/'+str(time)+'lat40x40']
                except:
                        print 'without '+nameStation[i]+' '+str(time)+'lat40x40'

                try:
                        del aotOut[satellite+'/'+nameStation[i]+'/'+year+'/lon40x40/'+str(time)+'lon40x40']
                except:
                        print 'without '+nameStation[i]+' '+str(time)+'lon40x40'

                try:
                        del aotOut[satellite+'/'+nameStation[i]+'/'+year+'/aotModel/'+str(time)+'aotModel']
                except:
                        print 'without '+nameStation[i]+' '+str(time)+'aotModel'

                try:
                        del aotOut[satellite+'/'+nameStation[i]+'/'+year+'/qFlagMat/'+str(time)+'qFlagMat']
                except:
                        print 'without '+nameStation[i]+' '+str(time)+'qFlagMat'




		print 'saida -> '+satellite+'/'+nameStation[i]+'/'+year+'/aot40x40/'+str(time)+'aot40x40'

	#	print aotModel[i]  
	
                aotOut[satellite+'/'+str(nameStation[i])+'/'+year+'/aot40x40/'+str(time)+'aot40x40']=aotArr40[i]
                aotOut[satellite+'/'+str(nameStation[i])+'/'+year+'/lat40x40/'+str(time)+'lat40x40']=latArr40[i]
                aotOut[satellite+'/'+str(nameStation[i])+'/'+year+'/lon40x40/'+str(time)+'lon40x40']=lonArr40[i]

		#print aotModel[i]
                aotOut[satellite+'/'+str(nameStation[i])+'/'+year+'/aotModel/'+str(time)+'aotModel']=aotModel[i]
		aotOut[satellite+'/'+str(nameStation[i])+'/'+year+'/qFlagMat/'+str(time)+'qFlagMat']=qFlagMat[i]


        aotOut.close()





#-----------------------------------------


##################### general ###########################

#------------------------------------------
# write file .h5 file
#
def writeData(pathOut,satellite,nameStation,year,time,aotArr40,latArr40,lonArr40):

        aotOut=h5.File(pathOut+'/'+'aotDataSet.h5')

        for i in range(len(nameStation)):

                try:
                        del aotOut[satellite+'/'+nameStation[i]+'/'+year+'/aot40x40/'+str(time)+'aot40x40']
                except:
                        print 'without '+nameStation[i]+' '+str(time)+'aot40x40'

                try:
                        del aotOut[satellite+'/'+nameStation[i]+'/'+year+'/lat40x40/'+str(time)+'lat40x40']
                except:
                        print 'without '+nameStation[i]+' '+str(time)+'lat40x40'

                try:
                        del aotOut[satellite+'/'+nameStation[i]+'/'+year+'/lon40x40/'+str(time)+'lon40x40']
                except:
                        print 'without '+nameStation[i]+' '+str(time)+'lon40x40'

		print 'saida -> '+satellite+'/'+nameStation[i]+'/'+year+'/aot40x40/'+str(time)+'aot40x40'
#		print aotArr40[i] 
                aotOut[satellite+'/'+str(nameStation[i])+'/'+year+'/aot40x40/'+str(time)+'aot40x40']=aotArr40[i]
                aotOut[satellite+'/'+str(nameStation[i])+'/'+year+'/lat40x40/'+str(time)+'lat40x40']=latArr40[i]
                aotOut[satellite+'/'+str(nameStation[i])+'/'+year+'/lon40x40/'+str(time)+'lon40x40']=lonArr40[i]


        aotOut.close()
#--------------------------------------


def writeDataTime(pathOut,year,timeArr,satellite,process):

        aotOut=h5.File(pathOut+'/'+'aotDataSet.h5')

        try:
                del aotOut['time'+'/'+year+'/'+satellite+process]
        except:
                print 'without timeSerie'

        aotOut['time'+'/'+year+'/'+satellite+process]=timeArr

        aotOut.close()


