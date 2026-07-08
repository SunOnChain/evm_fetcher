from analyzers.transfer import analyze as transfer
from analyzers.swap import analyze as swap
from analyzers.bridge import analyze as bridge
from analyzers.staking import analyze as staking
from analyzers.reward import analyze as reward


ANALYZERS = [
    swap,
    bridge,
    staking,
    reward,
    transfer,
]
