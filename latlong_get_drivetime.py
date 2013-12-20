from bs4 import BeautifulSoup
from urllib2 import urlopen
from time import sleep
import re
import pandas as pd
import numpy as np

def make_soup(url):
	return BeautifulSoup(urlopen(url).read(), "lxml")

def get_drive_time(url):
	timemin = 0
	try:
		soup = make_soup(url)
		time = soup.find(id='drivetime').get_text().encode('utf-8')
		if 'hour' in time:
			result = re.search('(?P<stuff>\d+) hour',time)
			timemin += int(result.group('stuff')) * 60
		if 'minute' in time:
			result = re.search('(?P<stuff>\d+) minute',time)
			timemin += int(result.group('stuff'))
		sleep(1)
	except urllib2.HTTPError, e:
	    timemin = None
	except urllib2.URLError, e:
	    timemin = None
	return timemin

if __name__ == '__main__':
	url = 'http://www.travelmath.com/driving-time/from/'
	centerLat = 47.6562513
	centerLong = -122.312971
	path = 'lat_long_water.csv'
	df = pd.read_csv(path)
	df = df.set_index('FID')
	if 'Timemin' not in df.columns:
		df['Timemin'] = None
	for x, row in df[df['WATER'] != 'Water'].iterrows(): #& (df['Timemin'] is None)
		print x
		df['Timemin'][x] = get_drive_time('{0}{1},{2}/to/{3},{4}'.format(url,row['Latitude'],row['Longitude'],centerLat,centerLong))
		if x % 10 == 0: df.to_csv(path, sep=',')
	df.to_csv(path, sep=',')
	