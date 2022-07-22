import re
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, PreferencesEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup

class FastTrackExtension(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(PreferencesEvent, PreferencesEventListener())
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class PreferencesEventListener(EventListener):

    def on_event(self, event, _):
        url = event.preferences['url']
        fast_track_results = query_fast_track_table(url)

        with open("./results.json", 'w+') as file:
            updated_data = {'query_date': str(datetime.today().date()), 'results': fast_track_results}
            json.dump(updated_data, file)


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        url = extension.preferences['url']
        fast_track_results = get_fast_track_table(url)

        items = []
        for description, date in fast_track_results:
            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name=date,
                                             description=description,
                                             on_enter=HideWindowAction()))

        return RenderResultListAction(items)

def get_fast_track_table(url):
    try:
        with open("./results.json", 'r+') as file:
            data = json.load(file)

            query_date = datetime.strptime(data['query_date'])
            if query_date < datetime.today():
                query_result = query_fast_track_table(url)
                updated_data = {'query_date': str(datetime.today().date()), 'result': query_result}
                json.dump(updated_data, file)
            else:
                return data['result']
    except:
        return query_fast_track_table(url)
        
def query_fast_track_table(url):
    response = requests.get(url)
    text = response.text
    data = BeautifulSoup(text, 'html.parser')

    table = data.find(id="table1")
    entries = table.find_all("tr")[1:]
    
    return list([sanitise(entry) for entry in entries])

def sanitise(entry):
    texts = [cell.text for cell in entry.find_all("td")]
    expression = "\W+"
    return tuple([re.sub(expression, ' ', text).strip() for text in texts])

if __name__ == '__main__':
    FastTrackExtension().run()