from scraper import scrape
from files import file_dump


def zwillio_scraper(location_list):
    """

    Function to trigger script

    args : location list from command line args

    returns : none
    """
    url_list = map(scrape.url_builder, location_list[1:len(location_list)])

    queue = list(url_list)

    while queue:
        url = queue.pop(0)
        parsed_html = scrape.parser(url)
        zillow_data, neighbours = scrape.filter_data(parsed_html, url)

        file_dump.csv_dump(zillow_data)
        file_dump.json_dump(zillow_data)

        neighbour_urls = map(scrape.url_builder, neighbours)
        for neighbour in list(neighbour_urls):
            queue.append(neighbour)

