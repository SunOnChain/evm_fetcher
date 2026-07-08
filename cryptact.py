import csv
from collections import defaultdict, Counter
from datetime import datetime, timezone
import re

INPUT  = 'ledger.csv'
OUTPUT = 'cryptact_custom.csv'
SOURCE = 'SOMNIA'

APPROVE_METHOD = '0x095ea7b3'

ALLOWED_SYMBOLS = {'SOMI', 'WSOMI', 'ARWSOMI', 'USDC.e', 'STSOMI'}

FIELDNAMES = [
    'Timestamp', 'Action', 'Source', 'Base', 'Volume',
    'Price', 'Counter', 'Fee', 'FeeCcy', 'Comment'
]


def load_ledger(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def fmt_ts(unix_str):
    try:
        dt = datetime.fromtimestamp(int(unix_str), tz=timezone.utc)
        return dt.strftime('%Y/%m/%d %H:%M:%S')
    except Exception:
        return str(unix_str)


def to_eth(wei_str):
    try:
        return float(wei_str) / 1e18
    except Exception:
        return 0.0


def to_token(amount_str, decimals_str):
    try:
        dec = int(decimals_str) if decimals_str else 18
        return float(amount_str) / (10 ** dec)
    except Exception:
        return 0.0


def calc_fee(row):
    try:
        gas_used  = float(row.get('gasUsed') or 0)
        gas_price = float(row.get('gasPrice') or 0)
        return gas_used * gas_price / 1e18
    except Exception:
        return 0.0


def fv(v):
    return f'{v:.8f}' if isinstance(v, float) else str(v)


def is_nft(row):
    return bool(row.get('tokenID'))


def is_erc20_token(row):
    return bool(row.get('tokenSymbol') and not row.get('tokenID'))


def is_allowed_symbol(raw_sym):
    """Return the canonical symbol if allowed, else None."""
    if not raw_sym:
        return None
    sym = raw_sym.strip()
    if sym in ALLOWED_SYMBOLS:
        return sym
    return None


def normalize_symbol(sym):
    """Normalize symbol for export (e.g. USDC.e -> USDC)."""
    if sym == 'USDC.e':
        return 'USDC'
    return sym


def method_label(row):
    fn  = row.get('functionName') or ''
    met = row.get('method') or ''
    mid = row.get('methodId') or ''
    return (fn or met or mid).lower().strip()


def make_row(timestamp, action, base, volume, price='', counter='JPY',
             fee=0.0, fee_ccy='JPY', comment=''):
    return {
        'Timestamp': timestamp,
        'Action':    action,
        'Source':    SOURCE,
        'Base':      normalize_symbol(base),
        'Volume':    fv(volume),
        'Price':     price,
        'Counter':   counter,
        'Fee':       fv(fee),
        'FeeCcy':    fee_ccy,
        'Comment':   comment,
    }


def process_group(hash_, rows, my_addresses):
    rows = [r for r in rows if (r.get('isError') or '0') == '0']
    if not rows:
        return []

    # Skip entire group if any NFT row present
    if any(is_nft(r) for r in rows):
        return []

    # Skip entire group if it contains ERC20 rows but none are allowed symbols
    erc20_rows = [r for r in rows if is_erc20_token(r)]
    if erc20_rows:
        allowed_erc20 = [r for r in erc20_rows
                         if is_allowed_symbol(r.get('tokenSymbol') or '')]
        if not allowed_erc20:
            return []
        erc20_rows = allowed_erc20

    primary = next(
        (r for r in rows
         if r.get('gasPrice') and not r.get('tokenSymbol') and not r.get('type')),
        rows[0]
    )

    timestamp = fmt_ts(primary.get('timeStamp') or '0')
    fee       = calc_fee(primary)
    comment   = hash_
    name      = method_label(primary)
    mid       = (primary.get('methodId') or '').lower().strip()

    if mid == APPROVE_METHOD or 'approve' in name:
        return []

    results = []

    internal_rows = [r for r in rows if r.get('type') or r.get('traceId')]
    native_val    = to_eth(primary.get('value') or '0')

    sender   = (primary.get('from') or '').lower()
    receiver = (primary.get('to') or '').lower()

    is_mine_sender   = sender in my_addresses
    is_mine_receiver = receiver in my_addresses

    # ------------------------------------------------------------------ #
    #  BUY – buyExactIn / buy* swap methods                               #
    # ------------------------------------------------------------------ #
    if 'buyexactin' in name or (
        name.split('(')[0].strip().startswith('buy') and erc20_rows
    ):
        for r in erc20_rows:
            sym = is_allowed_symbol(r.get('tokenSymbol') or '')
            if not sym:
                continue
            vol = to_token(
    r.get('tokenValue') or r.get('value') or '0',
    r.get('tokenDecimal') or '18'
)
            results.append(make_row(timestamp, 'BUY', sym, vol,
                                    fee=fee, comment=comment))
            fee = 0.0
        if not erc20_rows and native_val > 0:
            results.append(make_row(timestamp, 'BUY', 'MON', native_val,
                                    fee=fee, comment=comment))
        return results

    # ------------------------------------------------------------------ #
    #  SELL – sellExactIn / sell* swap methods                            #
    # ------------------------------------------------------------------ #
    if 'sellexactin' in name or (
        name.split('(')[0].strip().startswith('sell') and erc20_rows
    ):
        for r in erc20_rows:
            sym = is_allowed_symbol(r.get('tokenSymbol') or '')
            if not sym:
                continue
            vol = to_token(
                r.get('tokenValue') or r.get('value') or '0',
                r.get('tokenDecimal') or '18'
            )
            results.append(make_row(timestamp, 'SELL', sym, vol,
                                    fee=fee, comment=comment))
            fee = 0.0
        if not erc20_rows and native_val > 0:
            results.append(make_row(timestamp, 'SELL', 'MON', native_val,
                                    fee=fee, comment=comment))
        return results

    # ------------------------------------------------------------------ #
    #  ERC-20 token transfers (non-swap)                                  #
    # ------------------------------------------------------------------ #
    for r in erc20_rows:
        sym = is_allowed_symbol(r.get('tokenSymbol') or '')
        if not sym:
            continue
        vol = to_token(
            r.get('tokenValue') or r.get('value') or '0',
            r.get('tokenDecimal') or '18'
        )
        from_addr = (r.get('from') or '').lower()
        to_addr   = (r.get('to') or '').lower()

        if from_addr in my_addresses:
            action = 'PAY'
        elif to_addr in my_addresses:
            action = 'BONUS'
        else:
            action = 'BONUS'

        if vol > 0:
            results.append(make_row(timestamp, action, sym, vol,
                                    fee=fee, comment=comment))
            fee = 0.0

    if erc20_rows:
        return results

    # ------------------------------------------------------------------ #
    #  Native MON transfers                                               #
    # ------------------------------------------------------------------ #
    if native_val > 0:
        action = 'PAY' if is_mine_sender else 'BONUS'
        results.append(make_row(timestamp, action, 'MON', native_val,
                                fee=fee, comment=comment))
        fee = 0.0
        return results

    # ------------------------------------------------------------------ #
    #  Internal value transfers                                           #
    # ------------------------------------------------------------------ #
    for r in internal_rows:
        val = to_eth(r.get('value') or '0')
        if val <= 0:
            continue
        from_addr = (r.get('from') or '').lower()
        action = 'PAY' if from_addr in my_addresses else 'BONUS'
        results.append(make_row(timestamp, action, 'MON', val,
                                fee=fee, comment=comment))
        fee = 0.0

    if results:
        return results

    # ------------------------------------------------------------------ #
    #  Gas-only → SENDFEE                                                 #
    # ------------------------------------------------------------------ #
    if fee > 0:
        results.append(make_row(
            timestamp, 'SENDFEE', 'MON', fee,
            fee=0.0,
            comment=f'gas:{comment}'
        ))

    return results


def main():
    rows = load_ledger(INPUT)
    if not rows:
        print('No rows found in ledger.csv')
        return

    addr_counter = Counter()
    for r in rows:
        v = (r.get('from') or '').lower()
        if v:
            addr_counter[v] += 1

    my_addresses = set()
    if addr_counter:
        my_addresses.add(addr_counter.most_common(1)[0][0])

    for r in rows:
        v = (r.get('to') or '').lower()
        if v in my_addresses:
            my_addresses.add(v)

    groups = defaultdict(list)
    for r in rows:
        h = r.get('hash') or ''
        if h:
            groups[h].append(r)

    def group_sort_key(item):
        _, rs = item
        try:
            return int(rs[0].get('timeStamp') or 0)
        except Exception:
            return 0

    sorted_groups = sorted(groups.items(), key=group_sort_key)

    output_rows = []
    for hash_, group_rows in sorted_groups:
        out = process_group(hash_, group_rows, my_addresses)
        output_rows.extend(out)

    with open(OUTPUT, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(output_rows)

    print(f'Done. {len(output_rows)} rows written to {OUTPUT}')


if __name__ == '__main__':
    main()
