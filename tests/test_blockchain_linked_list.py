import pytest

from blockchain import GENESIS_PROOF, GENESIS_HASH
from blockchain.chain_implementations import LinkedListChain
from blockchain.models import Block


@pytest.fixture
def blockchain():
    return LinkedListChain()


class TestLinkedListChain:
    def test_add_block_and_len(self, blockchain):
        block = Block(index=1, timestamp=1234567890, transactions=[], proof=GENESIS_PROOF, previous_hash=GENESIS_HASH)
        blockchain.add_block(block)

        assert len(blockchain) == 1
        assert blockchain.last_block == block

    def test_chain_serializable(self, blockchain):
        block1 = Block(index=1, timestamp=1234567890, transactions=[], proof=GENESIS_PROOF, previous_hash=GENESIS_HASH)
        block2 = Block(index=2, timestamp=1234567891, transactions=[], proof=124, previous_hash="hash1")

        blockchain.add_block(block1)
        blockchain.add_block(block2)

        serialized_chain = blockchain.chain_serializable

        assert isinstance(serialized_chain, list)

    def test_get_block_by_index(self, blockchain):
        block1 = Block(index=1, timestamp=1234567890, transactions=[], proof=GENESIS_PROOF, previous_hash=GENESIS_HASH)
        block2 = Block(index=2, timestamp=1234567891, transactions=[], proof=124, previous_hash="hash1")

        blockchain.add_block(block1)
        blockchain.add_block(block2)

        # Retrieve block by index (0-based)
        block = blockchain.get_block_by_index(0)

        assert block.index == 1

    def test_repr(self, blockchain):
        block = Block(index=1, timestamp=1234567890, transactions=[], proof=GENESIS_PROOF, previous_hash=GENESIS_HASH)
        blockchain.add_block(block)

        assert repr(blockchain).startswith(LinkedListChain.__name__)
