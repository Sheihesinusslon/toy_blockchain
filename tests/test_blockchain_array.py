import pytest

from blockchain import GENESIS_HASH, GENESIS_PROOF
from blockchain.chain_implementations import ArrayChain
from blockchain.models import Block


class TestArrayChain:
    @pytest.fixture
    def array_chain(self):
        """Fixture to initialize the ArrayChain."""
        return ArrayChain()

    def test_add_block(self, array_chain):
        block = Block(index=1, timestamp=1234567890, transactions=[], proof=GENESIS_PROOF, previous_hash=GENESIS_HASH)
        array_chain.add_block(block)

        assert len(array_chain.chain) == 1
        assert array_chain.last_block == block

    def test_get_block_by_index(self, array_chain):
        block1 = Block(index=1, timestamp=1234567890, transactions=[], proof=GENESIS_PROOF, previous_hash=GENESIS_HASH)
        block2 = Block(index=2, timestamp=1234567891, transactions=[], proof=124, previous_hash="hash1")

        array_chain.add_block(block1)
        array_chain.add_block(block2)

        retrieved_block = array_chain.get_block_by_index(1)
        assert retrieved_block == block2

    def test_repr(self, array_chain):
        block = Block(index=1, timestamp=1234567890, transactions=[], proof=GENESIS_PROOF, previous_hash=GENESIS_HASH)
        array_chain.add_block(block)

        assert repr(array_chain).startswith(ArrayChain.__name__)

    def test_len(self, array_chain):
        assert len(array_chain) == 0

        block = Block(index=1, timestamp=1234567890, transactions=[], proof=GENESIS_PROOF, previous_hash=GENESIS_HASH)
        array_chain.add_block(block)

        assert len(array_chain) == 1
