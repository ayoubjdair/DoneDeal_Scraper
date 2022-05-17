import requests
import PySimpleGUI as sg
from bs4 import BeautifulSoup
from tabulate import tabulate

cars = []
titles = []
years = []
engines = []
milage = []
locations = []
prices = []
links = []

result = requests.get(
    "https://www.donedeal.ie/cars/Volkswagen/Scirocco?price_to=15000&sort=publishdate%20desc"
)

result2 = requests.get(
    "https://www.donedeal.ie/cars/Volkswagen/Scirocco?price_to=15000&sort=publishdate%20desc&start=28"
)


result3 = requests.get(
    "https://www.donedeal.ie/cars/Volkswagen/Scirocco?price_to=15000&sort=publishdate%20desc&start=60"
)

src = result.content
src2 = result2.content
src3 = result3.content

soup = BeautifulSoup(src, 'html.parser')
soup2 = BeautifulSoup(src2, 'html.parser')
soup3 = BeautifulSoup(src3, 'html.parser')

listing_titles = soup.find_all('p', attrs={'class' : 'card__body-title'})
listing_titles2 = soup2.find_all('p', attrs={'class' : 'card__body-title'})
listing_titles3 = soup3.find_all('p', attrs={'class' : 'card__body-title'})

listing_details = soup.find_all('ul', attrs={'class' : 'card__body-keyinfo'})
listing_details2 = soup2.find_all('ul', attrs={'class' : 'card__body-keyinfo'})
listing_details3 = soup3.find_all('ul', attrs={'class' : 'card__body-keyinfo'})

listing_prices = soup.find_all('div', attrs={'class' : 'card__price--left-options'})
listing_prices2 = soup2.find_all('div', attrs={'class' : 'card__price--left-options'})
listing_prices3 = soup3.find_all('div', attrs={'class' : 'card__price--left-options'})

listing_links = soup.find_all('a', attrs={'class' : 'card__link'})
listing_links2 = soup2.find_all('a', attrs={'class' : 'card__link'})
listing_links3 = soup3.find_all('a', attrs={'class' : 'card__link'})

for listing in listing_titles:
    try:
        title = listing.text
        titles.append(title)
    except:
        print("Oops! no Title Found...")
        continue

for listing in listing_details:
    try:
        years.append(listing.text[:4])
        engines.append(listing.text[4:14])
        milage.append(listing.text[14:23])
        locations.append(listing.text[23:])
    except:
        print("Error fetching details...")
        continue
    
for listing in listing_prices:
    try:
        price = listing.find('p', attrs={'class' : 'card__price'}).text
        prices.append(price)
    except:
        print("Error fetching price...")
        continue
    
for listing in listing_links:
    try:
        links.append(listing.attrs['href'])
    except:
        print("Error fetching link...")
        continue
    
# Page 2
for listing in listing_titles2:
    try:
        title = listing.text
        titles.append(title)
    except:
        print("Oops! no Title Found...")
        continue

for listing in listing_details2:
    try:
        years.append(listing.text[:4])
        engines.append(listing.text[4:14])
        milage.append(listing.text[14:23])
        locations.append(listing.text[23:])
    except:
        print("Error fetching details...")
        continue
    
for listing in listing_prices2:
    try:
        price = listing.find('p', attrs={'class' : 'card__price'}).text
        prices.append(price)
    except:
        print("Error fetching price...")
        continue
    
for listing in listing_links2:
    try:
        links.append(listing.attrs['href'])
    except:
        print("Error fetching link...")
        continue
    
    
# Page 3
for listing in listing_titles3:
    try:
        title = listing.text
        titles.append(title)
    except:
        print("Oops! no Title Found...")
        continue

for listing in listing_details3:
    try:
        years.append(listing.text[:4])
        engines.append(listing.text[4:14])
        milage.append(listing.text[14:23])
        locations.append(listing.text[23:])
    except:
        print("Error fetching details...")
        continue
    
for listing in listing_prices3:
    try:
        price = listing.find('p', attrs={'class' : 'card__price'}).text
        prices.append(price)
    except:
        print("Error fetching price...")
        continue
    
for listing in listing_links3:
    try:
        links.append(listing.attrs['href'])
    except:
        print("Error fetching link...")
        continue
    
for x in range(len(titles)):
    cars.append([titles[x], years[x], engines[x], milage[x], locations[x], prices[x], links[x]])
    # print(titles[x])
    # print(years[x])
    # print(engines[x])
    # print(milage[x])
    # print(locations[x])

print('                    TITLE                           YEAR    ENGINE     MILAGE         LOCATION        PRICE    LINKS')
print(tabulate(cars))

