#import pandas;
import matplotlib.pyplot as plt;
import numpy as np;

def loadData(fileName):
	carInformation = [];
	with open(fileName, 'r') as f:
		for line in f:
			line = line.replace('[', '');
			line = line.replace(']', '');
			line = line.replace('\n', '');
			data = line.split(',');	
			if ( int(data[4]) == -1 or int(data[5]) == -1):
				continue;
			carInformation.append({'make': fixString(data[0]), 'model': fixString(data[1]), 'line': fixString(data[2]), 'price': int(data[3]), 'year': int(data[4]), 'mileage': int(data[5])});
	return carInformation;		

def fixString(string):
	string = string.replace('\'','');
	string = string.lstrip();
	return string;

def find(searchString, columnName, dictionary, returnColumn=''):
	returnList = [];
	for item in dictionary:
		if (item[columnName] == searchString):
			if (returnColumn!=''):
				returnList.append(item[returnColumn]);
			else:
				returnList.append(item);
	return returnList;

def findUnique(columnName, dictionary):
	returnList = [];
	for item in dictionary:
		if (item[columnName] not in returnList):
			returnList.append(item[columnName]);
	returnList.sort();
	return returnList;

def interpolate(xpoints, ypoints):
	numCoeff = len(xpoints);
	mat = [];
	for x,y in zip(xpoints, ypoints):
		line = [];
		for power in list(reversed(range(0, numCoeff))):
			line.append(x ** power);
		line.append(y);	
		mat.append(line)
	matrix = np.array(mat);
	A = matrix[:,0:numCoeff];
	B = matrix[:,-1];
	coefficients = np.linalg.solve(A,B); 
	return coefficients;	

def evalInterpolation(x, y, xrange):
	cpoints =  interpolate(x,y);
	print cpoints
	xpoints = xrange;
	ypoints = [];
	for xp in xpoints:
		ytemp = 0;
		for p, c in zip(list(reversed(range(0, len(cpoints)))), cpoints):
			ytemp = ytemp + c * (xp ** p);
		ypoints.append(ytemp);
	return ypoints;	

def listMean(lst):
	N = len(lst);
	lSum = 0;
	for l in lst:
		lSum = lSum + l;
	return lSum/N;



carInformation = loadData('Mercedes-Benz.csv')
threeSeries = find('C-Class', 'model', carInformation);
#threeSeries = carInformation
threeSeriesLines = [];

for uniqueLine in findUnique('line', threeSeries):
	data = find(uniqueLine, 'line', threeSeries);
	carPrices = [c['price'] for c in data];
	carYear = [c['mileage'] for c in data];
	plt.figure();
	plt.scatter(carYear, carPrices);
	#plt.xlabel('Year');
	plt.xlabel('Mileage [km]');
	plt.ylabel('Price [ZAR]');
	plt.hold(True);
	#get the mean price for a particular year
	# priceMeansPerYear = [];
	# uniqueYears = findUnique('mileage', data);
	# for year in uniqueYears:
	# 	priceMeansPerYear.append(listMean(find(year, 'mileage', data, 'price')));
	# yearRange = np.linspace(uniqueYears[0], uniqueYears[-1], num=1000);
	# yearIntp = evalInterpolation(uniqueYears, priceMeansPerYear, yearRange);
	# plt.xlim(2000, 2019);
	# plt.plot(uniqueYears, priceMeansPerYear, 'r');
	# plt.plot(yearRange, yearIntp, 'g');
	plt.title(uniqueLine);
	plt.show();