document.addEventListener("DOMContentLoaded", () => {
  const chainContainer = document.querySelector(".chain");
  const transactionList = document.querySelector("#transaction-list");
  const transactionForm = document.querySelector("#transaction-form");
  const mineForm = document.querySelector("#mine-form");
  const chainStatusLight = document.querySelector("#chain-status-light");
  const chainStatusText = document.querySelector("#chain-status-text");

  // Notification handler
  const showNotification = (message, type = "success") => {
    const notification = document.createElement("div");
    notification.className = `notification ${type}`;
    notification.textContent = message;
    document.body.appendChild(notification);
    notification.style.display = "block";
    setTimeout(() => notification.remove(), 3000);
  };

  // Fetch blockchain data
  const fetchBlockchainData = async () => {
    const res = await fetch("/chain");
    const data = await res.json();
    const chain = data.chain;

    // Update blockchain display
    chainContainer.innerHTML = chain.map(block => `
      <div class="chain-block">
        <p><strong>Block #${block.index}</strong></p>
        <p><strong>Proof:</strong> ${block.proof}</p>
        <p><strong>Transactions:</strong> ${block.transactions.length}</p>
      </div>
    `).join("");

    // Check chain validity
    if (data.chain_valid) {
      chainStatusLight.style.backgroundColor = "green";
      chainStatusText.textContent = "Valid";
    } else {
      chainStatusLight.style.backgroundColor = "red";
      chainStatusText.textContent = "Invalid";
    }
  };

  // Fetch pending transactions
  const fetchPendingTransactions = async () => {
    const res = await fetch("/transactions/pending");
    const data = await res.json();
    transactionList.innerHTML = data.pending_transactions.map(tx => `
      <div class="transaction-item">
        <span><strong>Sender:</strong> ${tx.sender}</span>
        <span><strong>Recipient:</strong> ${tx.recipient}</span>
        <span><strong>Amount:</strong> ${tx.amount}</span>
      </div>
    `).join("");
  };

  // Handle form submissions
  transactionForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(transactionForm);
    const body = Object.fromEntries(formData.entries());
    const res = await fetch("/transactions/new", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    if (res.ok) {
      showNotification("Transaction submitted successfully!");
      transactionForm.reset();
      fetchPendingTransactions();
    } else {
      showNotification("Failed to submit transaction", "error");
    }
  });

  mineForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(mineForm);
    const body = Object.fromEntries(formData.entries());
    const res = await fetch("/mine", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    if (res.ok) {
      showNotification("New block mined!");
      mineForm.reset();
      fetchBlockchainData();
      fetchPendingTransactions();
    } else {
      showNotification("Failed to mine block", "error");
    }
  });

  // Initial fetch
  fetchBlockchainData();
  fetchPendingTransactions();
});