
import random, datetime

import requests, os, json
from urllib.parse import urlencode
from bs4 import BeautifulSoup


def getCIK(ticker: str) -> str:
    print('looking up CIK')
    # Get the absolute path of the directory containing this script
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the text file containing CIK data
    text_file_path = os.path.join(script_directory, 'tickers.json')
    ticker = ticker.upper()  # Just the way the file is formatted
    # Open the file formatted as below
    # Key: 'ticker', Val {'cik', 'title}
    with open(text_file_path, 'r') as file:
        data = json.loads(file.read())
        try:
            return data[ticker]['cik']
        except Exception:
            raise LookupError(f"Error retrieving CIK number for company {ticker}")

# returns hyperlink to a list of 10-Q files for a specific company ticker
# the year parameter is the highest year the list will include
# set randomize_count to true if making subsequent requests with different years,
# there is an issue with the website where changing the year itself will not yield new
# results unless another parameter is changed
def buildLink(year: int, formtype: str, cik: str, randomize_count=False) -> str:
    print('building link')
    base_url = "https://www.sec.gov/cgi-bin/browse-edgar"
    # start loading results from this year + 1 and before because
    # companies are late with Q4 reports
    dateb = str(year + 1) + "0303"
    print(dateb)
    params = {
        "action": "getcompany",
        "CIK": cik,
        "type": formtype,
        "dateb": dateb,
        "start": "",
        "output": "",
        "count": "1"
    }

    if randomize_count:
        params['count'] = str(random.random())

    encoded_params = urlencode(params)
    return base_url + '?' + encoded_params
