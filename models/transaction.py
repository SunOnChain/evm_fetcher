from dataclasses import dataclass, field
from typing import List, Optional

from models.event import Event


@dataclass
class Transaction:
    hash: str
    chain: str
    wallet: str
    timestamp: int

    block_number: int = 0

    events: List[Event] = field(default_factory=list)

    tx_type: Optional[str] = None

    def add_event(self, event: Event):
        self.events.append(event)

    @property
    def fee_events(self):
        return [e for e in self.events if e.is_fee]

    @property
    def asset_events(self):
        return [e for e in self.events if not e.is_fee]
