from ctypes import resize
import math
import webbrowser
import requests
import PySimpleGUI as sg
from bs4 import BeautifulSoup
from tabulate import tabulate

links = []

def DrawGUI():
    
    sg.theme('Reddit')
    
    layout = [
        [sg.Text('Enter DoneDeal Link'), sg.Input(default_text='Example: https://www.donedeal.ie/cars/Make/Model?', size=(60, 1), key='link'), sg.Text('Number Of Pages'), sg.Input(size=(5, 1), key='listings')],
        [sg.Output(size=(120, 40), font='Courier 12')],
        [sg.Button('Search')],
        [sg.Input(default_text='Listing #', size=(8, 1), key='listing'), sg.Button('View Online')],
        [sg.Button('Exit', button_color=('white', 'firebrick3'))],
        [sg.T('Made By Ayoub Jdair', font='12', justification='r', expand_x=True)]
    ]

    window = sg.Window("CarFinder", layout, element_justification='l')

    while True:
        event, values = window.read()
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
        if event == 'Search':
            if values['link'].startswith('Example: ') or values['link'] == '':
                print("Please Enter a valid link (Like the example above)")
                window.refresh()
            if values['listings'] == '':
                print("Please Enter a valid pages number to search through")
                print("HINT: Pages are located at the bottom of each page")
                window.refresh()
            else:
                link = values['link']
                listings = values['listings']
                output = runScraper(link, listings)
                window.refresh()
        if event == 'View Online':
            if values['listing'] == 'Listing #' or values['listing'] == '':
                print("Please Enter a valid listing number")
                window.refresh()
            else:
                index = int(values['listing'])
                webbrowser.open(links[index])
            
    window.close()

def runScraper(link, listings):
    
    cars = []
    titles = []
    years = []
    engines = []
    milage = []
    county = []
    time = []
    prices = []
    links.clear()
    
    root = link
    pageStart = "&start="
    pages = int(listings)

    # src = setResult(root).content
    # src = setResult(1, root, pageStart).content
    # soup = BeautifulSoup(src, 'html.parser')
    # results = soup.find_all('h2')
    # print(results)
    # print(results[:-1].text)
    # pages = (int(math.ceil(int()/27)))
    # print(pages)
    # https://www.donedeal.ie/cars/audi/a4?
    
    for x in range(1, pages):
        src = setResult(x, root, pageStart).content
        
        soup = BeautifulSoup(src, 'html.parser')

        listing_titles = soup.find_all('p', attrs={'class' : 'card__body-title'})
        listing_details = soup.find_all('ul', attrs={'class' : 'card__body-keyinfo'})
        listing_geo_details = soup.find_all('ul', attrs={'card__adinfo card__adinfo--is-grid-only'})
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
            except:
                print("Error fetching details...")
                continue
            
        for listing in listing_geo_details:
            try:
                letters = ''.join([i for i in listing.text if not i.isdigit()])
                nums = ''.join([i for i in listing.text if i.isdigit()])
            
                letters = listing.text.split()
                
                county.append(letters[0][:-1])
                listing_time = nums + " " + letters[1]
                time.append(listing_time)
            
            except:
                print("Error fetching time or location details...")
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
        cars.append([x, titles[x], years[x], engines[x], milage[x], county[x], time[x], prices[x]])

    print(' #                        TITLE                         YEAR    ENGINE      MILAGE    COUNTY     TIME     PRICE    ')
    # print(' 0  Volkswagen Scirocco Low Mileage..sport 2.0 TDI Ma   2015  2.0 Diesel  34,529 mi  Dublin     1 day    €19,450')
    print(tabulate(cars))

def setResult(start, root, pageStart):
    result = requests.get(
        root + pageStart + str(start)
    )
    return result

if __name__ == '__main__':
    DrawGUI()
