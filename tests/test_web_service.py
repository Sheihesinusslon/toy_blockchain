import pytest
from fastapi.testclient import TestClient
from fastapi import status

from blockchain.models import Transaction
from blockchain.blockchain_main import Blockchain
from blockchain.chain_implementations import ChainType

from src.web_service.api import app

client = TestClient(app)


@pytest.fixture(scope="module")
def setup_blockchain():
    """Fixture to initialize the blockchain before tests."""
    blockchain = Blockchain(chain_type=ChainType.ARRAY_CHAIN)
    return blockchain


class TestAPIs:
    def test_index(self):
        """Test the landing page."""
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK

    def test_mine_block(self, setup_blockchain):
        """Test the mining endpoint."""
        request_data = {"miner_address": "miner1_address"}
        response = client.post("/mine", json=request_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data
        assert data["message"] == "New Block Forged"

    def test_new_transaction(self, setup_blockchain):
        """Test adding a new transaction."""
        transaction = Transaction(sender="sender_address", recipient="recipient_address", amount=50.0)
        response = client.post("/transactions/new", json=transaction.model_dump())
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "Transaction will be added to Block" in data["message"]

    def test_get_pending_transactions(self, setup_blockchain):
        """Test getting the list of pending transactions."""
        response = client.get("/transactions/pending")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "pending_transactions" in data

    def test_full_chain(self, setup_blockchain):
        """Test getting the full blockchain."""
        response = client.get("/chain")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert isinstance(data["chain"], list)
        assert isinstance(data["length"], int)
        assert isinstance(data["chain_valid"], bool)
