from decimal import Decimal

from models.event import Event
from models.event_types import (
    UNKNOWN,
    NATIVE_TRANSFER,
    INTERNAL_TRANSFER,
    ERC20_TRANSFER,
    ERC721_TRANSFER,
    ERC1155_TRANSFER,
    GAS_FEE,
)


def build_event(row):
    event_type = UNKNOWN

    if row.get("traceId"):
        event_type = INTERNAL_TRANSFER

    elif row.get("tokenID") and row.get("tokenValue"):
        event_type = ERC1155_TRANSFER

    elif row.get("tokenID"):
        event_type = ERC721_TRANSFER

    elif row.get("tokenSymbol"):
        event_type = ERC20_TRANSFER

    else:
        event_type = NATIVE_TRANSFER

    return Event(
        event_type=event_type,
        asset=row.get("tokenSymbol") or "NATIVE",
        amount=Decimal(row.get("tokenValue") or row.get("value") or "0"),
        sender=row.get("from"),
        receiver=row.get("to"),
        contract=row.get("contractAddress"),
        token_id=row.get("tokenID"),
    )


def build_fee_event(row):
    gas_used = Decimal(row.get("gasUsed") or "0")
    gas_price = Decimal(row.get("gasPrice") or "0")

    return Event(
        event_type=GAS_FEE,
        asset="NATIVE",
        amount=gas_used * gas_price,
        sender=row.get("from"),
        receiver=None,
        is_fee=True,
    )
