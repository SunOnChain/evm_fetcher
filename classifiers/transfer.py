def is_transfer(group, my_addresses):
    incoming = False
    outgoing = False

    my_addresses = {a.lower() for a in my_addresses}

    for row in group:
        from_addr = (row.get("from") or "").lower()
        to_addr = (row.get("to") or "").lower()

        if from_addr in my_addresses:
            outgoing = True

        if to_addr in my_addresses:
            incoming = True

    if incoming and outgoing:
        return "SELF"

    if incoming:
        return "RECEIVE"

    if outgoing:
        return "SEND"

    return None
