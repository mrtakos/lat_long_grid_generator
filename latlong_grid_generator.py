from bs4 import BeautifulSoup
from urllib2 import urlopen
from time import sleep
import re

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
	url = 'http://www.travelmath.com/driving-time/from/'
	print 'Latitude,Longitude,Drivetime'

	for x in range(diameter):
		for y in range(diameter):
			cLat = oLat - increment * x
			cLong = oLong + increment * y
			time = get_drive_time('{0}{1},{2}/to/{3},{4}'.format(url,cLat,cLong,centerLat,centerLong))
			print '{0},{1},{2}'.format(cLat,cLong,time)
			sleep(3)

