# importing modules
import requests
from bs4 import BeautifulSoup
import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# URL for scrapping data
url = 'https://www.worldometers.info/coronavirus/countries-where-coronavirus-has-spread/'

# get URL html
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

data = []

# soup.find_all('td') will scrape every
# element in the url's table
data_iterator = iter(soup.find_all('td'))    

# data_iterator is the iterator of the table
# This loop will keep repeating till there is
# data available in the iterator
while True:
	try:
		country = next(data_iterator).text
		confirmed = next(data_iterator).text
		deaths = next(data_iterator).text
		region = next(data_iterator).text

		# For 'confirmed' and 'deaths',
		# make sure to remove the commas
		# and convert to int
		data.append((country, int(confirmed.replace(',', '')), int(deaths.replace(',', '')), region))

	# StopIteration error is raised when
	# there are no more elements left to
	# iterate through
	except StopIteration:
		break

# Sort the data by the number of confirmed cases
data.sort(key = lambda row: row[1], reverse = True)

fields = ['Country', 'Number of Cases', 'Deaths', 'Region']

#print(data)

with open(r'Covid19ScraperTest.csv', 'w') as csvfile:
	csvwriter = csv.writer(csvfile)
	csvwriter.writerow(fields)
	csvwriter.writerows(data)

df = pd.read_csv(r'Covid19ScraperTest.csv', header=0, nrows=10)

countries = list(df['Country'])
cases = list(df['Number of Cases'])
deaths = list(df['Deaths'])

barWidth = 0.25
br1 = np.arange(len(cases))
br2 = [x + barWidth for x in br1]

plt.bar(br1, cases, color ='r', width = barWidth, edgecolor ='grey', label ='Cases')
plt.bar(br2, deaths, color ='g', width = barWidth, edgecolor ='grey', label ='Deaths')

plt.xlabel('Countries', fontweight ='bold', fontsize = 15)
plt.ylabel('Population', fontweight ='bold', fontsize = 15)
plt.xticks([r + barWidth for r in range(len(cases))], countries)

plt.legend()
plt.show()
