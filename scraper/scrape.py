from bs4 import BeautifulSoup
import requests
import re

ZILLOW_BASE_URL = "https://www.zillow.com/"
ZILLOW_PAGE_URL = "/home-values/"


def parser(url: str) -> BeautifulSoup:
    """
    parser function parses the given url using html parser in beautifulsoup and urllib

    Args : url string type

    returns : beautifulsoup object
    """

    if not isinstance(url, str):
        raise TypeError("Expecting url as string. " + str(type(url)) + " given")

    req_headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.8',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/61.0.3163.100 Safari/537.36 '
    }

    with requests.Session() as s:
        source = s.get(url, headers=req_headers)

    if source.status_code == 200:
        soup = BeautifulSoup(source.content, 'html.parser')
        return soup
    else:
        print("Error in parser")
        print(source.status_code)


def url_builder(location: str) -> str:
    """
    Gets location string and builds a url

    args: location string

    returns : url string
    """

    if not isinstance(location, str):
        raise TypeError("Expecting location as string. " + str(type(location)) + " given")

    return ZILLOW_BASE_URL + str(location) + ZILLOW_PAGE_URL


def filter_data(parsed_html: BeautifulSoup, url: str) -> dict:
    """
    Function accepts beautifulsoup object and filters required data and makes an object


    args : beautifulsoup object (contains html data), url as a string (to extract location)

    returns : zillow data json/dictionary and list of neighbours of location
    """

    if not isinstance(parsed_html, BeautifulSoup):
        raise TypeError("parsed html should be BeautifulSoup type. " + str(type(parsed_html)) + "given")

    if not isinstance(url, str):
        raise TypeError("url should be a string. " + str(type(url)) + "given")

    zillow_data = {}
    # one year forecast and change
    forecast_change = []
    for li in parsed_html.find(id="region-info").ul:
        for i in li:
            forecast_change.append(str(i).strip().split())

    # median listing and median sale
    median_listing_sale = []
    for li in parsed_html.find(class_="zsg-content-section market-overview").find(class_="value-info-list").findAll(
            class_="value"):
        for i in li:
            median_listing_sale.append(str(i).strip().split())

    # avg days on market, neg equity, delinquency
    market_health = []
    for li in parsed_html.find(class_="zsg-content-section market-health").find(class_="value-info-list").findAll(
            class_="value"):
        for i in li:
            market_health.append(str(i).strip().split())

    # rent list price rent sqft
    rent_details = []
    for li in parsed_html.findAll(class_="zsg-content-section region-info")[1].find(class_="value-info-list").findAll(
            class_="value"):
        for i in li:
            rent_details.append(str(i).strip().split())

    # price sqft
    price_sqft = []
    for li in parsed_html.find(class_="zsg-content-section listing-to-sales").find(class_="value-info-list").findAll(
            class_="value"):
        for i in li:
            price_sqft.append(str(i).strip().split())

    # neighbours
    neighbours = []
    for link in parsed_html.find(class_="zsg-content-section nearby-regions").findAll('a'):
        neighbours.append(link["href"].replace('/home-values/', '').replace('/', ''))

    try:
        zillow_data["location"] = url.replace(ZILLOW_BASE_URL, "").replace(ZILLOW_PAGE_URL, "")
        zillow_data["url"] = url
        zillow_data["zillow_value"] = str(parsed_html.find(id="region-info").h2.text).replace('$', '').replace(',', '')

        zillow_data["one_year_change"] = str(forecast_change[1][0]).replace('%', '')
        zillow_data["one_year_forcast"] = str(forecast_change[4][0]).replace('%', '')

        zillow_data["market_temperature"] = parsed_html.find(class_="market-temperature").find(
            class_="zsg-h2").text.lower()
        zillow_data["price_sqft"] = str(price_sqft[0][0]).replace('$', '').replace(',', '')

        zillow_data["median_listing_price"] = str(median_listing_sale[2][0]).replace('$', '').replace(',', '')
        zillow_data["median_sale_price"] = str(median_listing_sale[3][0]).replace('$', '').replace(',', '')

        if len(market_health) == 1:
            print("passing")
            pass
        elif len(market_health) == 3:
            zillow_data["avg-days_on_market"] = market_health[0][0]
            zillow_data["negative_equity"] = str(round(float(market_health[1][0].replace('%', '')) / 100, 3))
            zillow_data["delinquency"] = str(round(float(market_health[2][0].replace('%', '')) / 100, 3))
        elif len(market_health) == 2:
            zillow_data["negative_equity"] = str(round(float(market_health[0][0].replace('%', '')) / 100, 3))
            zillow_data["delinquency"] = str(round(float(market_health[1][0].replace('%', '')) / 100, 3))
        else:
            print("passing")
            print(url)
            print(len(market_health))

        zillow_data["rent_list_price"] = str(rent_details[1][0]).replace('$', '').replace(',', '')
        zillow_data["rent_sqft"] = str(rent_details[2][0]).replace('$', '').replace(',', '')
    except(TypeError, KeyError, AttributeError) as e:
        pass

    return zillow_data, neighbours


if __name__ == '__main__':
    print("You are trying to run a module.")
    print("Please run main.py or read README.md")
