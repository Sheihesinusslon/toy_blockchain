from pathlib import Path

from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from blockchain.blockchain_main import Blockchain
from blockchain.chain_implementations import ChainType
from blockchain.models import Transaction, MineRequest

app = FastAPI(title="Blockchain API")
CURRENT_DIR = Path(__file__).parent
STATIC_DIR = CURRENT_DIR / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
blockchain = Blockchain(chain_type=ChainType.ARRAY_CHAIN)


@app.get("/", response_class=HTMLResponse)
def index():
    """Serve the landing page."""
    template_path = CURRENT_DIR / "templates" / "index.html"
    with open(template_path, "r") as f:
        return HTMLResponse(content=f.read())


@app.post("/mine", status_code=status.HTTP_200_OK)
def mine(request: MineRequest) -> dict:
    """Mining new block: find the proof of work, then add the block to the chain."""
    block = blockchain.mine_block(request.miner_address)

    return {
        "message": "New Block Forged",
        "index": block.index,
        "transactions": block.transactions,
        "proof": block.proof,
        "previous_hash": block.previous_hash,
    }


@app.post("/transactions/new", status_code=status.HTTP_201_CREATED)
def new_transaction(transaction: Transaction) -> dict:
    """Create a new transaction and add it to the blockchain."""
    index = blockchain.add_new_transaction(transaction)

    return {"message": f"Transaction will be added to Block {index}."}


@app.get("/transactions/pending", status_code=status.HTTP_200_OK)
def get_pending_transactions() -> dict:
    """Return a list of new transactions not yet written into the chain."""
    return {"pending_transactions": blockchain.mempool}


@app.get("/chain", status_code=status.HTTP_200_OK)
def full_chain() -> dict:
    """Return the full blockchain."""
    return {
        "chain": blockchain.chain.chain,
        "length": len(blockchain.chain),
        "chain_valid": blockchain.is_chain_valid(),
    }
