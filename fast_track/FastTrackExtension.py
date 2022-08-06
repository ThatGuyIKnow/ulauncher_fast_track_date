from .KeywordQueryEventListener import KeywordQueryEventListener

from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.event import KeywordQueryEvent


class FastTrackExtension(Extension):
    staticmethod
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
