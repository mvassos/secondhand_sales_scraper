import webscraper

import time

#file to automate date collection using the webscraper.py file

def collect(url):
    #worker function, runs webscraper.py then schedules itself again
    print("Scraping CL...")
    webscraper.main(url)

if __name__ == '__main__':
    url_start = input('Enter Start Url: ')
    start_time = time.time()

    while True:
        collect(url_start)
        time.sleep(900 - ((time.time() - start_time) % 900))

