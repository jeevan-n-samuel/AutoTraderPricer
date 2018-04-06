import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt;
from Tkinter import *


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

def listMean(lst):
	N = len(lst);
	lSum = 0;
	for l in lst:
		lSum = lSum + l;
	return lSum/N;

def calculateMeanPerVar(varString, data):
	meanPerVar = [];
	uniqueElements = findUnique(varString, data);
	for element in uniqueElements:
		meanPerVar.append(listMean(find(element, varString, data, 'price')));
	return meanPerVar;


class mclass:
    def __init__(self,  window):
    	self.fig = Figure(figsize=(6,6));
    	self.plotNumber = 0;
    	files = {'BMW.csv', 'Mercedes-Benz.csv'};
    	self.carInfo = [];
    	for f in files:
    		self.carInfo = self.carInfo+loadData(f);
    		#print self.carInfo;
    	self.carModels = findUnique('model', self.carInfo);	
    	self.carLines = findUnique('line', self.carInfo);
        self.selectedLine = StringVar();
        self.selectedModel = StringVar();

        self.window = window
        self.button = Button(window, text="Add to plot", command=self.plot);
        self.button.pack();
        self.btnClearFig = Button(window, text="Clear figure", command=self.plot);
        self.menu = OptionMenu(window, self.selectedLine, *self.carLines);
        self.menu.pack();
        # self.models = OptionMenu(window, self.selectedModel, *self.carModels);
        # self.models.pack();
	



    def plot(self):
    	colourList = ['b', 'r', 'g', 'm', 'k', 'c', 'y'];
    	
    	self.plotNumber = self.plotNumber + 1;
    	if ( self.plotNumber > 5 ):
    		self.plotNumber = 0;
    	carData = find(self.selectedLine.get(), 'line', self.carInfo);
    	pricePerMileage = calculateMeanPerVar('mileage', carData);
    	uniqueMileage = findUnique('mileage', carData);
    	pricePerYear = calculateMeanPerVar('year', carData);
    	uniqueYear = findUnique('year', carData);

    	print uniqueMileage;
    	print pricePerMileage;

        x=np.array ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        v= np.array ([16,16.31925,17.6394,16.003,17.2861,17.3131,19.1259,18.9694,22.0003,22.81226])
        p= np.array ([16.23697,     17.31653,     17.22094,     17.68631,     17.73641 ,    18.6368,
            19.32125,     19.31756 ,    21.20247  ,   22.41444   ,  22.11718  ,   22.12453])

        #plt.figure();
        plt.plot(np.array(uniqueMileage), np.array(pricePerMileage), colourList[self.plotNumber]);
        plt.xlabel('Mileage [Km]');
        plt.ylabel('Price [ZAR]');
        plt.hold(True);
        plt.show();

        # fig = self.fig;
        # a = fig.add_plot();
        # a.plot(np.array(uniqueMileage), np.array(pricePerMileage), colourList[self.plotNumber]);
        # a.hold('True');
        # a.set_ylabel("Price [ZAR]", fontsize=14);
        # a.set_xlabel("Mileage [Km]", fontsize=14);

        # canvas = FigureCanvasTkAgg(fig, master=self.window)
        # canvas.get_tk_widget().pack()
        # canvas.draw()

window= Tk()
start= mclass (window)
window.mainloop()		