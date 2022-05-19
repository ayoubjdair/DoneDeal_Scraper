from ctypes import resize
import webbrowser
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

def DrawGUI():
    
    sg.theme('Dark')
    
    layout = [
        [sg.Text('Enter DoneDeal Link '), sg.Input(default_text='Example: https://www.donedeal.ie/cars/Make/Model', size=(88, 1), key='link')],
        [sg.Output(size=(120, 20), font='Courier 12')],
        [sg.Button('Scrape')],
        [sg.Input(default_text='Listing #', size=(8, 1), key='listing'), sg.Button('View Online')],
        [sg.Button('Exit', button_color=('white', 'firebrick3'))]
    ]

    window = sg.Window("DoneDeal Scraper", layout)

    while True:
        event, values = window.read()
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
        if event == 'Scrape':
            if values['link'] == 'Example: https://www.donedeal.ie/cars/Make/Model' or values['link'] == '':
                print("Please Enter a valid link (Like the example above)")
                window.refresh()
            else:
                link = values['link']
                output = runScraper(link)
                window.refresh()
        if event == 'View Online':
            if values['listing'] == 'Listing #' or values['listing'] == '':
                print("Please Enter a valid listing number")
                window.refresh()
            else:
                index = int(values['listing'])
                webbrowser.open(links[index])
            
    window.close()

def runScraper(link):
    root = link
    pageStart = "&start="

    for x in range(1, 115, 23):
        src = setResult(x, root, pageStart).content
        
        soup = BeautifulSoup(src, 'html.parser')

        listing_titles = soup.find_all('p', attrs={'class' : 'card__body-title'})
        listing_details = soup.find_all('ul', attrs={'class' : 'card__body-keyinfo'})
        listing_prices = soup.find_all('div', attrs={'class' : 'card__price--left-options'})
        listing_links = soup.find_all('a', attrs={'class' : 'card__link'})


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


    for x in range(len(titles)):
        cars.append([x, titles[x], years[x], engines[x], milage[x], locations[x], prices[x]])

    print(' #                       TITLE                          YEAR    ENGINE      MILAGE        LOCATION       PRICE    ')
    print(tabulate(cars))

def setResult(start, root, pageStart):
    result = requests.get(
        root + pageStart + str(start)
    )
    return result

if __name__ == '__main__':
    DrawGUI()
