from bs4 import BeautifulSoup
from urllib2 import urlopen
from time import sleep
import re

if __name__ == '__main__':
	diameter = 75
	incrementMax = 0.75
	increment = incrementMax / diameter
	# 47.840353,-122.589684 Port Gamble
	# 47.6562513, -122.312971 Admissions
	centerLat = 47.6562513
	centerLong = -122.312971
	oLat = centerLat + (incrementMax / 2)
	oLong = centerLong - (incrementMax / 2)
	print 'Latitude,Longitude'

	for x in range(diameter):
		for y in range(diameter):
			cLat = oLat - increment * x
			cLong = oLong + increment * y
			print '{0},{1}'.format(cLat,cLong)

