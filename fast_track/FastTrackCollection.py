
from dataclasses import dataclass, field
from datetime import datetime
from email.policy import default
from typing import List, NamedTuple


class FastTrackResult(NamedTuple):
    date: str
    description: str


@dataclass
class FastTrackCollection:
    query_date: datetime = datetime.fromtimestamp(0)
    results: List[FastTrackResult] = field(default_factory=list)

    def __iter__(self) -> iter:
        return iter(self.results)
