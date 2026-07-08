from dataclasses import dataclass, field

from models.event import Event


@dataclass
class Transaction:
    hash: str
    chain: str
    wallet: str
    timestamp: int

    block_number: int = 0

    tx_type: str | None = None
    protocol: str | None = None
    category: str | None = None

    asset_events: list[Event] = field(default_factory=list)

    def add_event(self, event: Event):
        self.asset_events.append(event)
