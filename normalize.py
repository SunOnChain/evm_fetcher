import json
import csv

def load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, dict):
            return data.get('result', [])
        if isinstance(data, list):
            return data
        return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def s(val):
    return str(val).strip() if val is not None else ''

def set_method(current, candidate):
    if not current and candidate and s(candidate):
        return s(candidate)
    return current

transactions = load_json('transactions.json')
internal     = load_json('internal.json')
erc20        = load_json('erc20.json')
erc721       = load_json('erc721.json')
erc1155      = load_json('erc1155.json')

tx_map = {}

for r in transactions:
    h = s(r.get('hash', ''))
    if not h:
        continue
    tx_map[h] = {
        'hash':             h,
        'blockNumber':      s(r.get('blockNumber')),
        'timeStamp':        s(r.get('timeStamp')),
        'from':             s(r.get('from')),
        'to':               s(r.get('to')),
        'value':            s(r.get('value')),
        'gas':              s(r.get('gas')),
        'gasUsed':          s(r.get('gasUsed')),
        'gasPrice':         s(r.get('gasPrice')),
        'isError':          s(r.get('isError')),
        'txreceipt_status': s(r.get('txreceipt_status')),
        'contractAddress':  s(r.get('contractAddress')),
        'input':            s(r.get('input')),
        'methodId':         s(r.get('methodId')),
        'functionName':     s(r.get('functionName')),
        'method':           '',
        'tokenName':        '',
        'tokenSymbol':      '',
        'tokenDecimal':     '',
        'tokenID':          '',
        'tokenValue':       '',
        'type':             '',
        'traceId':          '',
        'errCode':          '',
    }

def _base_entry(h, r):
    return {
        'hash':             h,
        'blockNumber':      s(r.get('blockNumber')),
        'timeStamp':        s(r.get('timeStamp')),
        'from':             s(r.get('from')),
        'to':               s(r.get('to')),
        'value':            s(r.get('value')),
        'gas':              s(r.get('gas')),
        'gasUsed':          s(r.get('gasUsed')),
        'gasPrice':         s(r.get('gasPrice', '')),
        'isError':          s(r.get('isError', '')),
        'txreceipt_status': '',
        'contractAddress':  s(r.get('contractAddress')),
        'input':            '',
        'methodId':         s(r.get('methodId', '')),
        'functionName':     s(r.get('functionName', '')),
        'method':           '',
        'tokenName':        '',
        'tokenSymbol':      '',
        'tokenDecimal':     '',
        'tokenID':          '',
        'tokenValue':       '',
        'type':             '',
        'traceId':          '',
        'errCode':          '',
    }

def merge_token(records, tx_map, kind):
    for r in records:
        h = s(r.get('hash', ''))
        if not h:
            continue
        if h not in tx_map:
            tx_map[h] = _base_entry(h, r)
        e = tx_map[h]
        if not e['tokenName']:
            e['tokenName']    = s(r.get('tokenName'))
        if not e['tokenSymbol']:
            e['tokenSymbol']  = s(r.get('tokenSymbol'))
        if not e['tokenDecimal']:
            e['tokenDecimal'] = s(r.get('tokenDecimal'))
        if kind == 'erc20':
            if not e['tokenValue']:
                e['tokenValue'] = s(r.get('value'))

        if kind == 'erc1155':
            if not e['tokenValue']:
                e['tokenValue'] = s(r.get('tokenValue'))
            if not e['tokenValue']:
                e['tokenValue'] = s(r.get('tokenValue'))
        if not e['contractAddress']:
            e['contractAddress'] = s(r.get('contractAddress'))
        if not e['blockNumber']:
            e['blockNumber'] = s(r.get('blockNumber'))
        if not e['timeStamp']:
            e['timeStamp'] = s(r.get('timeStamp'))

merge_token(erc20,   tx_map, 'erc20')
merge_token(erc721,  tx_map, 'erc721')
merge_token(erc1155, tx_map, 'erc1155')

for r in internal:
    h = s(r.get('hash', ''))
    if not h:
        continue
    if h not in tx_map:
        tx_map[h] = _base_entry(h, r)
        tx_map[h]['type']    = s(r.get('type'))
        tx_map[h]['traceId'] = s(r.get('traceId'))
        tx_map[h]['errCode'] = s(r.get('errCode'))
    else:
        e = tx_map[h]
        if not e['type']:
            e['type']    = s(r.get('type'))
        if not e['traceId']:
            e['traceId'] = s(r.get('traceId'))
        if not e['errCode']:
            e['errCode'] = s(r.get('errCode'))

# Collect per-hash method candidates
erc20_fn    = {}
erc721_fn   = {}
erc1155_fn  = {}
internal_fn = {}
tx_mid      = {}
erc20_mid   = {}

for r in erc20:
    h = s(r.get('hash', ''))
    if h and h not in erc20_fn:
        erc20_fn[h]  = s(r.get('functionName'))
        erc20_mid[h] = s(r.get('methodId'))

for r in erc721:
    h = s(r.get('hash', ''))
    if h and h not in erc721_fn:
        erc721_fn[h] = s(r.get('functionName'))

for r in erc1155:
    h = s(r.get('hash', ''))
    if h and h not in erc1155_fn:
        erc1155_fn[h] = s(r.get('functionName'))

for r in internal:
    h = s(r.get('hash', ''))
    if h and h not in internal_fn:
        internal_fn[h] = s(r.get('functionName'))

for r in transactions:
    h = s(r.get('hash', ''))
    if h:
        tx_mid[h] = s(r.get('methodId'))

for h, e in tx_map.items():
    m = e['method']
    m = set_method(m, erc20_fn.get(h, ''))
    m = set_method(m, erc721_fn.get(h, ''))
    m = set_method(m, erc1155_fn.get(h, ''))
    m = set_method(m, internal_fn.get(h, ''))
    m = set_method(m, tx_mid.get(h, ''))
    m = set_method(m, erc20_mid.get(h, ''))
    e['method'] = m

fieldnames = [
    'hash', 'blockNumber', 'timeStamp', 'from', 'to', 'value',
    'gas', 'gasUsed', 'gasPrice', 'isError', 'txreceipt_status',
    'contractAddress', 'input', 'methodId', 'functionName', 'method',
    'tokenName', 'tokenSymbol', 'tokenDecimal', 'tokenID', 'tokenValue',
    'type', 'traceId', 'errCode',
]

rows = sorted(tx_map.values(), key=lambda x: (x['timeStamp'], x['hash']))

with open('ledger.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Done. {len(rows)} transactions written to ledger.csv.")
