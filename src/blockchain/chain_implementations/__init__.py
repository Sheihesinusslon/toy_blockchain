from enum import Enum
from typing import Union

from blockchain.chain_implementations.blockchain_array import ArrayChain
from blockchain.chain_implementations.blockchain_linked_list import LinkedListChain
from blockchain.chain_implementations.interface import ChainProtocol

Chain = Union[ArrayChain, LinkedListChain, ChainProtocol]


class ChainType(str, Enum):
    ARRAY_CHAIN = "array"
    LINKED_LIST_CHAIN = "linked_list"
    GRAPH_CHAIN = "graph"


def create_chain(chain_type: ChainType) -> Chain:
    match chain_type:
        case ChainType.ARRAY_CHAIN:
            return ArrayChain()
        case ChainType.LINKED_LIST_CHAIN:
            return LinkedListChain()
