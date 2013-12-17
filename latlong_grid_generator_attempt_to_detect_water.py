from bs4 import BeautifulSoup
from urllib2 import urlopen
from time import sleep
from osgeo import ogr, osr, gdal
import re

drv = ogr.GetDriverByName('ESRI Shapefile') #We will load a shape file
ds_in = drv.Open("wtrbdy_det.shp")    #Get the contents of the shape file
lyr_in = ds_in.GetLayer(0)    #Get the shape file's first layer

#Put the title of the field you are interested in here
idx_reg = lyr_in.GetLayerDefn().GetFieldIndex("WATER")

#If the latitude/longitude we're going to use is not in the projection
#of the shapefile, then we will get erroneous results.
#The following assumes that the latitude longitude is in WGS84
#This is identified by the number "4236", as in "EPSG:4326"
#We will create a transformation between this and the shapefile's
#project, whatever it may be
geo_ref = osr.SpatialReference()
geo_ref.ImportFromEPSG(2926)
point_ref = osr.SpatialReference()
point_ref.ImportFromEPSG(4236)
ctran = osr.CoordinateTransformation(point_ref,geo_ref)

def make_soup(url):
	return BeautifulSoup(urlopen(url).read(), "lxml")

def get_drive_time(url):
	soup = make_soup(url)
	time = soup.find(id='drivetime').get_text().encode('utf-8')
	timemin = 0
	if 'hour' in time:
		result = re.search('(?P<stuff>\d+) hour',time)
		timemin += int(result.group('stuff')) * 60
	if 'minute' in time:
		result = re.search('(?P<stuff>\d+) minute',time)
		timemin += int(result.group('stuff'))
	return timemin

def check_water(lon, lat):
    #Transform incoming longitude/latitude to the shapefile's projection
    [lon,lat,z] = ctran.TransformPoint(lon,lat,0.0)
    pt = ogr.Geometry(ogr.wkbPoint)
    pt.SetPoint_2D(0, lon, lat)

    #Set up a spatial filter such that the only features we see when we
    #loop through "lyr_in" are those which overlap the point defined above
    lyr_in.SetSpatialFilter(pt)

    #Loop through the overlapped features and display the field of interest
    for feat_in in lyr_in:
        print lon, lat, feat_in.GetFieldAsString(9)

if __name__ == '__main__':
	diameter = 75
	incrementMax = 0.75
	increment = incrementMax / diameter
	# 47.840353,-122.589684 Port Gamble
	# 47.6562513, -122.312971 Admissions
	centerLat = 47.6562513
	centerLong = -122.312971
	oLat = centerLat + incrementMax / 2
	oLong = centerLong - incrementMax / 2
	url = 'http://www.travelmath.com/driving-time/from/'
	print 'Latitude,Longitude,Drivetime'
	cLat = oLat
	cLong = oLong
	#print '{0},{1}'.format(cLat,cLong)

	for x in range(diameter):
		for y in range(diameter):
			cLat = oLat-increment*x
			cLong = oLong+increment*y
			water = check_water(cLong,cLat)
			#pt = Point('{0}, {1}'.format(cLat,cLong))
			#(new_place,new_point) = g.reverse(pt)
			#time = get_drive_time('{0}{1},{2}/to/{3},{4}'.format(url,cLat,cLong,centerLat,centerLong))
			#time = 0
			#print '{0},{1},{2}'.format(cLat,cLong,time)
			#sleep(1)

