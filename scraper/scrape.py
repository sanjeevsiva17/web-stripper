from bs4 import BeautifulSoup
import requests
import sys
import json

ZILLOW_BASE_URL = "https://www.zillow.com/"
ZILLOW_PAGE_URL = "/home-values/"


def parser(url: str) -> BeautifulSoup:
    """
    parser function parses the given url using html parser in beautifulsoup and urllib
    Gets url as parameter and returns beautifulsoup object
    """

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

    soup = BeautifulSoup(source.content, 'html.parser')
    return soup


def url_builder(location: str) -> str:
    """
    Gets location string and builds a url
    """

    return ZILLOW_BASE_URL + str(location) + ZILLOW_PAGE_URL


def filter_data(parsed_html: BeautifulSoup, url: str) -> dict:
    """
    Function accepts beautifulsoup object and filters required data and makes an object
    """

    zillow_data = {}
    # one year forecast and change
    x = []
    for li in parsed_html.find(id="region-info").ul:
        for i in li:
            x.append(str(i).strip().split())

    # median listing and median sale
    y = []
    for li in parsed_html.find(class_="zsg-content-section market-overview").find(class_="value-info-list").findAll(
            class_="value"):
        for i in li:
            y.append(str(i).strip().split())

    # avg days on market, neg equity, delinquency
    z = []
    for li in parsed_html.find(class_="zsg-content-section market-health").find(class_="value-info-list").findAll(
            class_="value"):
        for i in li:
            z.append(str(i).strip().split())

    # rent list price rent sqft
    w = []
    for li in parsed_html.findAll(class_="zsg-content-section region-info")[1].find(class_="value-info-list").findAll(
            class_="value"):
        for i in li:
            w.append(str(i).strip().split())

    # price sqft
    v = []
    for li in parsed_html.find(class_="zsg-content-section listing-to-sales").find(class_="value-info-list").findAll(
            class_="value"):
        for i in li:
            v.append(str(i).strip().split())

    # neighbours
    neighbours = []
    for link in parsed_html.find(class_="zsg-content-section nearby-regions").findAll('a'):
        neighbours.append(link["href"].replace('/home-values/', '').replace('/', ''))

    try:
        zillow_data["location"] = url.replace(ZILLOW_BASE_URL, "").replace(ZILLOW_PAGE_URL, "")
        zillow_data["url"] = url
        zillow_data["zillow_value"] = parsed_html.find(id="region-info").h2.text
        zillow_data["one_year_change:"] = x[1][0]
        zillow_data["one_year_forcast"] = x[4][0]
        zillow_data["market_temperature"] = parsed_html.find(class_="market-temperature").find(class_="zsg-h2").text
        zillow_data["price_sqft"] = v[0][0]
        zillow_data["median_listing_price"] = y[2][0]
        zillow_data["median_sale_price"] = y[3][0]
        zillow_data["avg-days_on_market"] = z[0][0]
        zillow_data["negative_equity"] = z[1][0]
        zillow_data["delinquency"] = z[2][0]
        zillow_data["rent_list_price"] = w[1][0]
        zillow_data["rent_sqft"] = w[2][0]
    except(TypeError, KeyError, AttributeError) as e:
        pass

    return zillow_data, neighbours


def csv_dump(data):


def json_dump(data):
    json_object = json.dumps(data, indent=4)
    location = data["location"]

    with open("zillowInsight-" + location + ".json", "w") as outfile:
        outfile.write(json_object)



location_list = sys.argv
url_list = map(url_builder, location_list[1:len(location_list)])

queue = list(url_list)

while queue:
    url = queue.pop(0)
    parsed_html = parser(url)
    zillow_data, neighbours = filter_data(parsed_html, url)
    print(zillow_data)
    csv_dump(zillow_data)
    json_dump(zillow_data)
    neighbour_urls = map(url_builder, neighbours)
    for neighbour in list(neighbour_urls):
        queue.append(neighbour)
