import json
from csv import DictWriter


def csv_dump(data: dict):
    """
    Gets zillow data as parameters and Creates a csv file

    args: json/dict object

    returns none
    """
    location = data["location"]
    with open('csv/zillowInsight-' + location + ".csv", 'w') as f:
        csv_writer = DictWriter(f, fieldnames=['location', 'url', 'zillow_value', 'one_year_change', 'one_year_forcast',
                                               'market_temperature', 'price_sqft', 'median_listing_price',
                                               'median_sale_price', 'avg-days_on_market', 'negative_equity',
                                               'delinquency', 'rent_list_price', 'rent_sqft'])
        csv_writer.writeheader()
        csv_writer.writerow(data)


def json_dump(data: dict):
    """
    Gets Zillow data as parameter and creates a json file

    args: dictionary object

    returns : None
    """
    json_object = json.dumps(data, indent=4)
    location = data["location"]

    with open("json/zillowInsight-" + location + ".json", "w") as outfile:
        outfile.write(json_object)


if __name__ == '__main__':
    print("You are trying to run a module.")
    print("Please run main.py or read README.md")