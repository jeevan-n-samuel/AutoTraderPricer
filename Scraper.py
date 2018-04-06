# import libraries
import urllib2
import os
from bs4 import BeautifulSoup

def PriceStringToNumber(price):
	price = price.replace('R', '');
	price = price.replace(',', '');
	price = price.replace('+VAT', '');
	price = price.strip();

	if (price == 'POA'):
		return -1;
	else:
		return int(price);
	return -1;

def MileageToNumber(mileage):
	mileage = mileage.replace('Km', '');
	mileage = mileage.replace(',', '');
	return int(mileage);

def GetCarLine(carMakeAndModel, carTitle):
	carMakeAndModel = carMakeAndModel.replace(carTitle, '');
	carBits = carMakeAndModel.split(' ');
	return carBits[1];

def ExtractCarData(carTitleAndPrice, carDetails, carMake, carModel):
	#get name and price
	carName = carTitleAndPrice.find('h2').text;
	carPrice = carTitleAndPrice.find('div', attrs={'class': 'col-xs-5 col-sm-3 listing-item-price text-right'}).text;
	#further process the car price to a number
	carPrice = PriceStringToNumber(carPrice);
	carDetails = carDetails.find_all('li');
	carYear = -1;
	carMileage = -1;
	if (len(carDetails) > 2):
		if (carDetails[0].text.isnumeric()):
			carYear = int(carDetails[0].text);
		if (carDetails[1].text.find('Km')>0):
			carMileage = MileageToNumber(carDetails[1].text);

	carLine = GetCarLine(carName, carMake + ' ' + carModel).upper();
	carInfo = [carMake, carModel, str(carLine), carPrice, carYear, carMileage];

	return carInfo;

def dealWithURLSpaces(urlString):
	return urlString.replace(' ', '%20');



#the data to scrape
makes = ['BMW', 'Kia'];
models = [
			
			['1 Series', '3 Series'],
			['Rio']

		];
pagesToSearch = [1, 5, 9, 14, 19, 24, 29, 34, 39, 44, 49, 54, 59, 64];

makeCount = 0;

for make in makes:
	print make
	fileToWrite = open(make+'.csv','w');
	for model in models[makeCount]:
		for page in pagesToSearch:
			quote_page = 'https://www.autotrader.co.za/perpage/60/makemodel/make/'+dealWithURLSpaces(make.upper())+'/model/'+dealWithURLSpaces(model.upper())+'/page/'+str(page)+'/search';
			webPage = urllib2.urlopen(quote_page);
			soup = BeautifulSoup(webPage, 'html.parser');
			car_title_and_price = soup.find_all('div', attrs={'class': 'row listing-item-title-wrapper'});
			car_listing_data = soup.find_all('ul', attrs={'class': 'listing-item-specs'});
			for car, listing_data in zip(car_title_and_price, car_listing_data):
				carInfo = ExtractCarData(car, listing_data, make, model);
				print carInfo;
				print >> fileToWrite, carInfo;
	fileToWrite.close();
	makeCount = makeCount+1;



