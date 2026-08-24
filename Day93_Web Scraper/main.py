# Alibaba scraper
# make csv file
# find all aria-label tags
# Put them in csv
# profit

with open("raw_data.html", "r", encoding="utf-8") as file:
    data = file.read()

from bs4 import BeautifulSoup
import csv

soup = BeautifulSoup(data, "html.parser")

listings = []

for listing in soup.find_all("a"):
    a = [str(listing['aria-label'])]
    listings.append(a)

print(listings)

with open('extracted_listings.csv', 'w', newline='', encoding='utf-8') as result:
    wr = csv.writer(result, dialect='excel')
    wr.writerows(listings)