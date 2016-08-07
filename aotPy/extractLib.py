import numpy as np

def DoDegResolutionX(deltaX):

    earthRay = 6371.    
    #lonRes = (deltaX * 360)/ (2 * np.pi * earthRay * np.cos((lat * np.pi)/180.))
    lonRes = (deltaX * 360)/ (2 * np.pi * earthRay)

    return lonRes

def DoDegResolutionY(deltaY):
    
    earthRay = 6371
    latRes = (deltaY * 360)/ (2 * np.pi * earthRay)
    
    return latRes


