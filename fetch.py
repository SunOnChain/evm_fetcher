from fetchers import FETCHERS

from fetchers.somnia import fetch as blockscout_fetch
from fetchers.etherscan import fetch as etherscan_fetch

FETCHERS["blockscout"] = blockscout_fetch
FETCHERS["etherscan"] = etherscan_fetch


def fetch(chain_info, address):
    fetcher = chain_info["fetcher"]

    if fetcher not in FETCHERS:
        raise Exception(f"No fetcher registered for '{fetcher}'")

    return FETCHERS[fetcher](chain_info, address)
