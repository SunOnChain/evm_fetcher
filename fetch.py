from fetchers.somnia import fetch as somnia_fetch


def fetch(chain, address):
    if chain == "somnia":
        return somnia_fetch(chain, address)

    raise Exception(f"Unsupported chain: {chain}")
