import hashlib
from time import time
from typing import List

from blockchain import TRANSACTION_FEE_PERCENTAGE, NETWORK_SENDER, MINER_REWARD, BINGO, GENESIS_HASH, GENESIS_PROOF
from blockchain.chain_implementations import Chain, ChainType, create_chain
from blockchain.exceptions import MiningException
from blockchain.models import Block, HashString, Transaction


class Blockchain:
    def __init__(self, chain_type: ChainType):
        self.chain: Chain = create_chain(chain_type)
        self.mempool: List[Transaction] = []
        self.create_genesis_block()

    def create_genesis_block(self) -> None:
        """Create the first block in the blockchain (genesis block)."""
        _ = self.create_new_block(previous_hash=GENESIS_HASH, proof=GENESIS_PROOF)

    def create_new_block(self, previous_hash: HashString, proof: int) -> Block:
        """Create a new block and reset the mempool."""
        block = Block(
            index=len(self.chain) + 1,
            timestamp=int(time()),
            transactions=self.mempool,
            proof=proof,
            previous_hash=previous_hash,
        )

        self.mempool = []
        self.chain.add_block(block)
        return block

    def add_new_transaction(self, transaction: Transaction) -> int:
        """Add a new transaction to the mempool."""
        self.mempool.append(transaction)
        return self.chain.last_block.index + 1

    @staticmethod
    def hash_(block: Block) -> HashString:
        """Hash a block using SHA-256."""
        block_str = block.model_dump_json().encode()
        return HashString(hashlib.sha256(block_str).hexdigest())

    def proof_of_work(self, last_proof: int) -> int:
        """Find a valid proof of work."""
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof: int, proof: int) -> bool:
        guess = f"{last_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == BINGO

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            previous_block = self.chain.get_block_by_index(i - 1)
            current_block = self.chain.get_block_by_index(i)

            if current_block.previous_hash != self.hash_(previous_block):
                return False

            if not self.valid_proof(previous_block.proof, current_block.proof):
                return False

        return True

    def calculate_transaction_fees(self) -> float:
        """Calculate the total transaction fees in the mempool."""
        fee_percentage = TRANSACTION_FEE_PERCENTAGE / 100
        return sum(tx.amount * fee_percentage for tx in self.mempool)

    def mine_block(self, miner_address: str) -> Block:
        """Mine a new block, including the reward transaction for the miner."""
        if not self.is_chain_valid():
            raise MiningException("Blockchain is invalid. Cannot mine a new block.")

        last_block = self.chain.last_block
        proof = self.proof_of_work(last_block.proof)

        previous_hash = self.hash_(last_block)

        total_reward = MINER_REWARD + self.calculate_transaction_fees()

        reward_transaction = Transaction(
            sender=NETWORK_SENDER,
            recipient=miner_address,
            amount=total_reward,
        )
        self.add_new_transaction(reward_transaction)

        return self.create_new_block(previous_hash, proof)
