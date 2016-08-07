import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


from mpl_toolkits.basemap import Basemap
from mpl_toolkits.basemap import maskoceans
from matplotlib.patches import Polygon



#color definition

cdict = {'red':   [(0.0,  0.0, 0.95),          
                   (1.0,  0.0, 0)],

         'green': [(0.0,  0.0, 0.95),
                   (1.0,  0.0, 0)],

         'blue':  [(0.0,  0.0, 0.95),
                   (1.0,  0.0, 0)]}

myGrey = mpl.colors.LinearSegmentedColormap('my_colormap',cdict,256)


def drawScreen(beginLat,endLat,beginLon,endLon,m):
    lats = [endLat,beginLat,beginLat,endLat]#
    #lats = [beginLat,endLat,endLat,beginLat]
    lons = [endLon,endLon,beginLon,beginLon]#beginLon,beginLon,endLon,endLon
    x, y = m( lons, lats )
    xy = zip(x,y)
    poly = Polygon( xy, facecolor='red', alpha=0.5 )
    plt.gca().add_patch(poly)


def writeKML(figName,beginLatFig, endLatFig, beginLonFig, endLonFig):
   
    #Meu figName tem a seguinte forma /User/.../.../test
    #o .kml será /User/.../.../test.kml
    #para este caso o sufix seria: test
    
    sufix = figName.split('/')[-1]
    
    fileKml = open(figName+'.kml','w')
    output = "<?xml version='1.0' encoding='UTF-8'?><kml xmlns='http://earth.google.com/kml/2.0'><Document><LookAt id='"+sufix+".KMZ'><longitude>-55.0</longitude><latitude>-9.0</latitude><range>1.2770075427617017E7</range><tilt>0.0000</tilt><heading>0.0000</heading></LookAt><GroundOverlay><name>"+sufix+"</name><Icon><href>"+sufix+".png</href></Icon><LatLonBox id='"+sufix+".KMZ'><north>"+str(endLatFig)+"</north><east>"+str(endLonFig)+"</east><south>"+str(beginLatFig)+"</south><west>"+str(beginLonFig)+"</west></LatLonBox></GroundOverlay><ScreenOverlay><name>DSA - CPTEC</name><Icon><href>logoDsa.png</href></Icon><overlayXY x='0' y='1' xunits='fraction' yunits='fraction'/><screenXY x='0' y='1' xunits='fraction' yunits='fraction'/><rotationXY x='0' y='0' xunits='fraction' yunits='fraction'/><size x='0' y='0' xunits='fraction' yunits='fraction'/></ScreenOverlay></Document></kml>" 
    
    fileKml.write(output)
    fileKml.close()

def doPlotGoogleEarth(lon,lat,aeroOptDep,title,figName,beginLatFig=-60,endLatFig=20,beginLonFig=-96,endLonFig=-13,\
beginLatReg=0,endLatReg=0,beginLonReg=0,endLonReg=0):

        writeKML(figName,beginLatFig, endLatFig, beginLonFig, endLonFig)
        
        m=Basemap(projection='cyl',resolution='l',llcrnrlat=beginLatFig,\
urcrnrlat=endLatFig,llcrnrlon=beginLonFig,urcrnrlon=endLonFig)

        parallels = np.arange(beginLatFig,endLatFig,(endLatFig-beginLatFig)/8.)
        meridians = np.arange(beginLonFig,endLonFig,(endLonFig-beginLonFig)/4.)
        m.drawcountries(linewidth=0.1)
        m.drawcoastlines(linewidth=0.1)
        m.pcolormesh(lon,lat,aeroOptDep,vmin=0.,vmax=1.)
        #m.drawlsmask(ocean_color = 'w', resolution = 'l')
        
        if beginLatReg==0 and endLatReg==0 and beginLonReg==0 and endLonReg==0:
                pass

        else:   
                drawScreen(beginLatReg,endLatReg,beginLonReg,endLonReg,m)
                #print beginLatReg,endLatReg,beginLonReg,endLonReg
        #cb=m.colorbar()
        #plt.title(title)
        
        plt.tight_layout()
        plt.savefig(figName+'.png',format='png',dpi=300, transparent=True,  bbox_inches='tight',  pad_inches=0)
        plt.clf()
        
        
        
        #plt.show()
#----------------------

def doPlot(lon,lat,aeroOptDep,title,figName,minData,maxData,beginLatFig=-60,endLatFig=20,beginLonFig=-96,\
endLonFig=-13,beginLatReg=0,endLatReg=0,beginLonReg=0,endLonReg=0):

        plt.figure(figsize=(15,15))
        m=Basemap(projection='cyl',resolution='l',llcrnrlat=beginLatFig,\
urcrnrlat=endLatFig,llcrnrlon=beginLonFig,urcrnrlon=endLonFig)
      
        print figName
        parallels = np.arange(beginLatFig,endLatFig,(endLatFig-beginLatFig)/8.)
        meridians = np.arange(beginLonFig,endLonFig,(endLonFig-beginLonFig)/4.)
        m.drawcountries(linewidth=0.5,color = 'k')
        m.drawcoastlines(linewidth=0.5, color ='k')
        
        if title[:13] == 'VIIRS - MODIS':
            #cmap = plt.get_cmap('my_cmap')
            #cmap = plt.get_cmap('coolwarm')
            cmap = myCmap
            
        else:
            #cmap = plt.get_cmap('Oranges')
            cmap = plt.get_cmap('jet')
            #cmap = myGrey
        
        aeroOptDep = maskoceans(lon, lat, aeroOptDep)
        #m.drawmapboundary(fill_color='black')
        
        m.pcolormesh(lon,lat,aeroOptDep,vmin=minData,vmax=maxData, cmap = cmap)
        
	if beginLatReg==0 and endLatReg==0 and beginLonReg==0 and endLonReg==0:
                pass

        else:   
                drawScreen(beginLatReg,endLatReg,beginLonReg,endLonReg,m)
                cb=m.colorbar()
        plt.title(title)
        plt.savefig(figName+'.png',format='png',dpi=300,transparent=True)
        plt.clf()
        #plt.show()
#-------------------------




