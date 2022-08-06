
from .FastTrackCollection import FastTrackCollection, FastTrackResult

from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup, ResultSet

class KeywordQueryEventListener(EventListener):
    def __init__(self):
        self.stored_results = FastTrackCollection()

    def on_event(self, event, extension):
        url = extension.preferences['url']
        fast_track_results = self.get_fast_track_table(url)

        items = []
        for date, description in fast_track_results:
            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name=date,
                                             description=description,
                                             on_enter=HideWindowAction()))

        return RenderResultListAction(items)

    def get_fast_track_table(self, url: str) -> FastTrackCollection:
        # Compare the current date to the queried date. Initiate query if they do not match.
        query_date = self.stored_results.query_date
        today = datetime.today().date()
        if query_date != today:
            self.stored_results = self.query_fast_track_table(url)
        return self.stored_results
            
    def query_fast_track_table(self, url: str) -> FastTrackCollection:
        # Send a query for the site and parse the results using BS4
        response = requests.get(url)
        text = response.text
        data = BeautifulSoup(text, 'html.parser')

        # Find the table with id "table1" (This table contains the relevant dates)
        table = data.find(id="table1")
        # Skip the first row in the table as it contains headers.
        results = table.find_all("tr")[1:]
        # Sanitise all the rows for HTML chars, special chars, etc.
        results = list([self.sanitise(entry) for entry in results])
        # Get the current date (Without the time of day)
        query_date = datetime.today().date()

        return FastTrackCollection(query_date, results)

    def sanitise(self, entry: ResultSet) -> FastTrackResult:
        # Extract all the text from each table cell
        texts = [cell.text for cell in entry.find_all("td")]
        # Replace all special characters with spaces
        expression = "\W+"
        desciption, date = (re.sub(expression, ' ', text).strip() for text in texts)
        return FastTrackResult(date=date, description=desciption)
