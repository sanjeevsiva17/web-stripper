import sys
import start

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("")
        print("provide location as arguments like the example below")
        print("python main.py corona-heights-san-francisco-ca")
        print("")
    start.zwillio_scraper(sys.argv)
