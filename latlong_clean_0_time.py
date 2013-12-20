import pandas as pd
import numpy as np

path = 'lat_long_water.csv'
df = pd.read_csv(path)
df = df.set_index('FID')
for x, row in df[(df['WATER'] != 'Water') & (df['Timemin'] == 0)].iterrows():
	if (df['Timemin'][x-1] - df['Timemin'][x] > 20) & (df['Timemin'][x+1] - df['Timemin'][x] > 20):
		print df['Timemin'][x-1], df['Timemin'][x], df['Timemin'][x+1]
		df['Timemin'][x] = int((df['Timemin'][x-1]+df['Timemin'][x-1])/2)
df.to_csv(path, sep=',')