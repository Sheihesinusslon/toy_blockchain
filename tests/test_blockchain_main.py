import pytest
from blockchain.blockchain_main import Blockchain
from blockchain.chain_implementations import ChainType
from blockchain.models import Transaction
from blockchain.exceptions import MiningException
from blockchain import GENESIS_HASH, GENESIS_PROOF, TRANSACTION_FEE_PERCENTAGE


@pytest.fixture
def blockchain():
    """Fixture to initialize the blockchain."""
    return Blockchain(chain_type=ChainType.ARRAY_CHAIN)


class TestBlockchain:
    def test_create_genesis_block(self, blockchain):
        assert len(blockchain.chain) == 1
        assert blockchain.chain.get_block_by_index(0).previous_hash == GENESIS_HASH
        assert blockchain.chain.get_block_by_index(0).proof == GENESIS_PROOF

    def test_add_new_transaction(self, blockchain):
        transaction = Transaction(sender="sender1", recipient="recipient1", amount=100)
        index = blockchain.add_new_transaction(transaction)

        assert index == 2
        assert len(blockchain.mempool) == 1  # Mempool should have the added transaction

    def test_is_chain_valid(self, blockchain):
        assert blockchain.is_chain_valid()

        transaction = Transaction(sender="sender2", recipient="recipient2", amount=50)
        blockchain.add_new_transaction(transaction)
        blockchain.mine_block(miner_address="miner1")

        assert blockchain.is_chain_valid()

    def test_proof_of_work(self, blockchain):
        last_proof = blockchain.chain.last_block.proof
        proof = blockchain.proof_of_work(last_proof)

        assert proof > 0  # Proof should be greater than 0
        assert blockchain.valid_proof(last_proof, proof)  # Proof should be valid

    def test_mine_block(self, blockchain):
        miner_address = "miner1"
        initial_chain_length = len(blockchain.chain)

        transaction = Transaction(sender="sender3", recipient="recipient3", amount=30)
        blockchain.add_new_transaction(transaction)
        block = blockchain.mine_block(miner_address)

        assert len(blockchain.chain) == initial_chain_length + 1
        assert block.transactions[-1].recipient == miner_address
        assert block.transactions[-1].amount > 0

    def test_invalid_chain_cannot_mine(self, blockchain):
        blockchain.create_new_block(previous_hash=GENESIS_HASH, proof=12345)
        blockchain.chain.get_block_by_index(0).previous_hash = "invalid_hash"

        with pytest.raises(MiningException):
            blockchain.mine_block(miner_address="miner1")

    def test_calculate_transaction_fees(self, blockchain):
        transaction1 = Transaction(sender="sender1", recipient="recipient1", amount=100)
        transaction2 = Transaction(sender="sender2", recipient="recipient2", amount=200)

        blockchain.add_new_transaction(transaction1)
        blockchain.add_new_transaction(transaction2)

        fees = blockchain.calculate_transaction_fees()
        expected_fees = (100 * TRANSACTION_FEE_PERCENTAGE / 100) + (200 * TRANSACTION_FEE_PERCENTAGE / 100)

        assert fees == expected_fees
