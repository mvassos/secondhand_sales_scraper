# Created by Manny Vassos
import urllib.request as urlReq
from bs4 import BeautifulSoup as soup
import re


def create_new_url(page_soup, url_base, firstpage):
    # finds new search modifier from next button
    # and slap it on the basic url
    if firstpage is 0:
        lower_button_soup = page_soup.find("div", {"class": "paginator buttongroup firstpage"})
    else:
        lower_button_soup = page_soup.find("div", {"class": "paginator buttongroup"})

    next_button_soup = lower_button_soup.find("a", {"class": "button next"})
    url_mod = str(next_button_soup["href"])
    # create next url to search for results
    url_next = url_base + url_mod
    return url_next


def get_all_results(page_soup, url_base):
    # check to see if another page of results exists...
    button_info = page_soup.find("span", "button pagenum")
    range_current = int(button_info.find("span", "rangeTo").text)
    range_goal = int(button_info.find("span", "totalcount").text)
    print("reading", range_current, "of", range_goal)
    # get initial results before next page is discovered (if needed to)
    results = page_soup.find_all("li", {"result-row"})
    print("size of results:", len(results))
    firstpage = 0

    while range_current != range_goal:
        # if more results exist on another page, grab next page
        url_next = create_new_url(page_soup, url_base, firstpage)
        firstpage = 1
        # read new page and get html
        uClient = urlReq.urlopen(url_next)
        page_html = uClient.read()
        uClient.close()
        page_soup = soup(page_html, "html.parser")
        # discover new pages results
        results_new = page_soup.find_all("li", {"result-row"})
        results = results + results_new
        print("size of results:", len(results))
        # get new item ranges from buttons!
        button_info = page_soup.find("span", "button pagenum")
        range_current = int(button_info.find("span", "rangeTo").text)
        range_goal = int(button_info.find("span", "totalcount").text)
        print("reading", range_current, "of", range_goal)

    return results


def get_results_info(results, search):
    count = len(results)
    print("found", count, " results")

    price_sum = 0

    for result in results:
        # begin parsing with soup information for each result
        price = (result.find("span", {"result-price"})).text
        title = (result.p.a).text.lower()
        title_list = title.split(' ')

        #remove results that dont have query words in the title
        if any(word in search for word in title_list):

            # OOF, didnt need to implement so much re...
            # regular expressions for isolating data
            price = int(re.search("\d+", price).group())
            # title = re.search("\>(.*)\<", title).group()
            # title = re.search("[^>].*[^<]", title).group()

            #filter out garbage for averages
            if price < 5:
                count -= 1
            else:
                price_sum += price

            print("\n" + title)
            print("$" + str(price))
        else:
            count -= 1

    price_avg = round(price_sum / count, 2)
    print("\nAverage price for your selection: $" + str(price_avg), "from", count, "results!")


def main():
    #url_start = input("Enter a Craigslist search url:\n")

    url_start = 'https://sfbay.craigslist.org/search/cta?query=2000+dodge+cummins'

    #find exact seach phrase
    eq_index = str(url_start).find('=') + 1
    query_raw = str(url_start)[eq_index:len(str(url_start))]
    query_list = query_raw.split('+')
    print("You searched for", query_raw)
    print(query_list)


    # isolate the base of the url to modify later (add new endings)
    url_base = re.search("(.*)(.org)", str(url_start)).group()

    uClient = urlReq.urlopen(url_start)

    # stores raw html file into a variable
    page_html = uClient.read()

    # close the url request client
    uClient.close()

    # storing html source into a soup type to do parsing
    page_soup = soup(page_html, "html.parser")
    # call worker function to get all results from multiple pages
    results = get_all_results(page_soup, url_base)

    get_results_info(results, query_list)


if __name__ == '__main__':
    main()
