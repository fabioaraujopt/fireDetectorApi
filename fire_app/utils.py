#REQUIRE TO INSTALL FOLLOWING DEPENDENCIES
#!pip install gpsphoto
#!pip install exifread

from GPSPhoto import gpsphoto
import numpy as np
from uuid import uuid4
import os

##Get Image GPSData from exif
##Returns dict {'Latitude': 38.6588703, 'Longitude': -9.2054545, 'Altitude': 102.23}
##Returns False (image have no exif data, image do not exist)
def getGpsData(imagePath):
    data=gpsphoto.getGPSData(imagePath)
    if(data==None):
    	return False
    else:
        return data

##Calculate Ground Sample Distance in px/cm^2
##ratio depends on the camera (23.2 MicasenseAltium)
##Returns float
def gsdCalculator(altitude,ratio = 23.2):
  return (altitude/ratio)*(altitude/ratio)
  

##Calculate MaskArea in px
##Returns list with mask areas
def getMaskAreaPixels(maskList):
	maskArea = list()
	for i in np.arange(np.array(maskList).shape[-1]): 
		maskArea.append(np.sum(maskList[:,:,i]))
	return maskArea
		
	
##Calculate MaskAreas in cm^2
##Return list with areas in cm^2
def getMaskAreaCmSquare(maskAreasList,gsd):
  maskAreas=list()
  for mask in maskAreasList:
    maskAreas.append(mask * gsd)
  return maskAreas

##return coordinates in pixels for the center of 
##a given ROI
def getRoiCenterPoint(roi): 
    x1=r['rois'][0][0]
    y1=r['rois'][0][1]
    x2=r['rois'][0][2]
    y2=r['rois'][0][3]
    
    return [((x2-x1)/2)+x1,((y2-y1/2)+y1] 


def convertImage(imagePath,convertedType='jpg'):
   random_token=str(uuid4())
   print("convert "+imagePath+" -colorspace RGB converted_images/"+random_token+".jpg")
   os.system("convert "+imagePath+" -colorspace RGB converted_images/"+random_token+".jpg ")
   return random_token+'.jpg'



