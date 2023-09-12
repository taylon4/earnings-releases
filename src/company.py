from src import utils
from bs4 import BeautifulSoup
import requests, datetime


class Company:
    def __init__(self, ticker: str):
        self.cik = utils.getCIK(ticker)
        self.ticker = ticker

    # return link to specific quarterly report given company ticker
    def getQuarterlyReport(self, year: int, quarter: str) -> str:
        # build a link to the list of reports, randomize_count=True -> see buildLink definition
        link = utils.buildLink(year, '10-q', self.cik, randomize_count=True)
        print('sending request')
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"}
        content = requests.get(url=link, headers=headers).content
        soup = BeautifulSoup(content, 'html.parser')
        print('rows retrieved')
        print(link)

        # find all rows of reports
        rows = soup.find_all('tr')

        # get the index of the appropriate report, top rows are neglected
        # top report starts at index 5
        index = 0

        # we first have to check if the search is within the current year
        current_year = datetime.datetime.now().year
        if current_year < year:
            raise ValueError("Year is too far in the future")

        print(current_year)

        match quarter.upper():
            case "Q4":
                index += 5
                if len(rows) < 6:
                    raise IndexError(f"No report found for {self.ticker} Q4")
            case "Q3":
                index += 6
                if len(rows) < 7:
                    raise IndexError(f"No report found for {self.ticker} Q3")
            case "Q2":
                index += 7
                if len(rows) < 8:
                    raise IndexError(f"No report found for {self.ticker} Q2")
            case "Q1":
                index += 8
                if len(rows) < 9:
                    raise IndexError(f"No report found for {self.ticker} Q1")
            case _:
                raise ValueError("Quarter must be Q1, Q2, Q3, or Q4")

        # now get the report page containing multiple file links
        req = requests.get("https://www.sec.gov" + rows[index].find_next('a')['href'], headers=headers)
        report = req.content
        report_soup = BeautifulSoup(report, 'html.parser')

        # find the row that has the 10-q
        for row in report_soup.find_all('tr'):
            if "10-q" in row.getText().lower():
                # third index is the link to the report
                return "https://www.sec.gov" + row.find('a')['href']

        raise IndexError(f"No 10-q report found at {req.url}")
