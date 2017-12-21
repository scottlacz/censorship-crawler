"""
This script will send a search query to Baidu and scrape the HTML looking for signs of censorship.
Queries are generated based on random lines grabbed from a list of 4.5 million Wikipedia titles.


CREDITS (Thanks for the help!):
File with Wikipedia titles courtesy of this StackOverflow question:
https://stackoverflow.com/questions/24474288/how-to-obtain-a-list-of-titles-of-all-wikipedia-articles

get_random_line function adapted from this StackOverflow question:
https://stackoverflow.com/questions/14924721/how-to-choose-a-random-line-from-a-text-file

Inspiration for how to make a web scraper:
https://medium.freecodecamp.org/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe

How to use a proxy with requests module:
https://stackoverflow.com/questions/8287628/proxies-with-python-requests-module#8287752

List of Chinese proxies:
https://www.proxynova.com/proxy-server-list/country-cn/

eventlet for timing out a request:
https://stackoverflow.com/questions/21965484/timeout-for-python-requests-get-entire-response
"""

import requests, os, random, time, eventlet
from sys import argv
from bs4 import BeautifulSoup


def get_random_title(file_name):
	"""Returns a random, complete line from a file."""
	total_bytes = os.stat(file_name).st_size 
	random_point = random.randint(0, total_bytes)
	with open(file_name) as file:
		file.seek(random_point)
		file.readline() # skip this line to clear the partial line
		return file.readline().rstrip('\n').replace('_', ' ').replace(',', '')


def scrape(title):
	"""Request HTML data through a proxy."""
	http_proxy = "http://124.88.67.31:80" # Chinese Server
	https_proxy = "https://201.151.178.235:8080" # Mexico Server (test)

	proxyDict = {
		"http"	: http_proxy,
		"https"	: https_proxy
	}
	response_check = False
	url = "http://www.baidu.com/s?wd=" + title # https not working properly.
	print("Please Wait. Requesting page...")
	while response_check == False:
		with eventlet.Timeout(5): # If a request takes longer than 5 seconds, it will timeout.
			response = requests.get(url)
			# response = request.get(url, proxies=proxyDict)
			response_check = True
		if response_check:	
			print("Request received.")
			return response.text
		else:
			print("Request failed. Retrying...")


def parse(html):
	"""Parse through the HTML data looking for the tag that says you got censored."""
	censor = False
	soup = BeautifulSoup(html, "lxml")
	print("Parsing HTML.")
	# Use BeautifulSoup to look for indication of censorship.
	# If any indication is found, censor = True.
	# print(soup.find_all("div", class_="result c-container ")) <- used for testing
	if censor == False:
		print("Parsing complete. No censorship found.")
	else:
		print("Parsing complete. CENSORSHIP DETECTED.")	
	return str(censor)
	

def write_censored(word, cen):
	"""Creates and appends to a csv file to log whether a word was censored or not."""
	print("Writing to file.")
	with open("censored.csv", 'a') as file:
		file.write(word + ',' + cen + "\n")
	print("Successfully saved to file.")


script, MAX_REQUESTS = argv

eventlet.monkey_patch()

for x in range(0, int(MAX_REQUESTS)):
	random_title = get_random_title("enwiki-latest-all-titles-in-ns0")
	write_censored(random_title, parse(scrape(random_title)))
	print("Total requests made: " + str(x+1))
	time.sleep(2) # Delay for 2 seconds before going again.

print("Script completed successfully.")
