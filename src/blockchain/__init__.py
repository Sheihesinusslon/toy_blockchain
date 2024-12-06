from typing import Final

from blockchain.models import HashString

NETWORK_SENDER: Final[str] = "network"
MINER_REWARD: Final[int] = 1
TRANSACTION_FEE_PERCENTAGE: Final[int] = 1
BINGO: Final[str] = "0000"

GENESIS_HASH: Final[HashString] = HashString("1")
GENESIS_PROOF: Final[int] = 1
