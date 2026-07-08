from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass
class Event:
    event_type: str

    asset: Optional[str] = None
    amount: Decimal = Decimal("0")

    sender: Optional[str] = None
    receiver: Optional[str] = None

    contract: Optional[str] = None
    token_id: Optional[str] = None

    is_fee: bool = False
