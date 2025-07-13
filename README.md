
# 🚦 EtherFineChain – Blockchain-Based Traffic Violation Management System

![EtherFineChain Banner](https://your-banner-url-if-any)

> A decentralized, transparent, and tamper-proof system for traffic violation enforcement using Ethereum Smart Contracts, IPFS, and Web3 technologies.

---

## 📌 Overview

Traffic enforcement systems in India and other countries face major issues including:
- Corruption
- Manual and error-prone processes
- Lack of transparency
- Absence of immutable records

**EtherFineChain** is a blockchain-based system that automates the logging of traffic violations, stores violation evidence securely via IPFS, and enables transparent penalty enforcement through Ethereum smart contracts.

---

## 🚀 Features

- ✅ **Decentralized Violation Logging** using Ethereum Smart Contracts  
- 🖼️ **Tamper-proof Evidence Storage** with IPFS via Pinata  
- ⚙️ **Automated Penalty Calculation and Ether Deduction**  
- 🔐 **Role-Based Access** (Violator & Authority separation)  
- 📊 **Real-World Simulation Dataset** (Red-light, No-helmet, Overspeeding)  
- 🌐 **Frontend Dashboard for Authority**  
- 📈 **Performance Benchmarked** (Gas, Latency, TPS)

---

## 📷 Project Demo

Coming Soon! (Include video/gif/screenshots)

---

## 🛠️ Tech Stack

| Category         | Tools Used                          |
|------------------|-------------------------------------|
| **Blockchain**   | Ethereum, Ganache, MetaMask         |
| **Storage**      | IPFS via Pinata                     |
| **Web3**         | Web3.js                             |
| **Frontend**     | HTML5, Tailwind CSS, JavaScript     |
| **IDE/Dev Tools**| VS Code, Remix IDE                  |
| **Test Setup**   | Windows 10, Chrome, i3 CPU, 12GB RAM|

---

## 📂 Dataset

Simulated dataset of 22 records with:
- 📸 JPG/PNG images (from traffic cams)
- 📄 Metadata JSON:
  - Vehicle Number
  - Violation Type
  - Camera ID
  - Location Coordinates
  - Timestamp
  - Penalty Amount

Each image is hashed (SHA-256), uploaded to IPFS via Pinata, and logged to the Ethereum blockchain with metadata.

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/etherfinechain.git
cd etherfinechain
````

### 2. Install Dependencies

```bash
npm install
```

### 3. Setup Ganache (Local Ethereum Blockchain)

* Download Ganache: [https://trufflesuite.com/ganache/](https://trufflesuite.com/ganache/)
* Start the workspace and copy RPC URL & accounts.

### 4. Deploy Smart Contract (Using Remix)

* Open `contract/EtherFineChain.sol` in Remix IDE.
* Use "Injected Web3" (MetaMask) and deploy the contract.
* Copy the contract address for frontend integration.

### 5. Configure MetaMask

* Add Custom RPC (Ganache settings)
* Import test accounts using private keys
* Fund authority account with test ETH

### 6. Run the Frontend

```bash
live-server frontend/
```

---

## 🧪 Smart Contract Functions

* `addViolation(vehicleId, timestamp, ipfsHash, violationType)`
* `getViolations()`
* `payPenalty(violationId)`

All records are stored immutably on-chain, enabling audit trails and real-time updates.

---

## 📊 Performance Metrics

| Metric         | Value         |
| -------------- | ------------- |
| Avg. Latency   | 134.48 ms     |
| Avg. Gas Usage | 314,726 units |
| Avg. TPS       | 7.36 tx/sec   |

---

## ⚠️ Limitations

* Public blockchain reveals metadata (no encryption yet)
* IPFS file pinning relies on Pinata (subject to garbage collection)
* No AI verification of evidence (future work)
* Smart contracts are not upgradeable post-deployment

---

## 💡 Future Improvements

* 🔍 AI/ML-based violation verification
* 📸 Live camera feed integration
* 🔗 National vehicle database sync
* 📲 Mobile version for authority users
* ⚡ Layer-2 scaling (Polygon, Optimism, etc.)

---

## 👤 Author

**Mainak Pal**
CSE, JGEC | SIP 2025
[LinkedIn](https://www.linkedin.com/in/mainak-pal/) • [GitHub](https://github.com/your-username) • [Email](mailto:your.email@example.com)

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙌 Acknowledgements

* Prof. **Jhuma Dutta**, Assistant Professor, CSE, JGEC
* Dr. **Subhas Barman**, HOD, CSE, JGEC
* Inspired by India’s Smart City Mission and CivicTech goals

---

## ⭐ Show Your Support

If you found this project helpful, consider giving it a ⭐ on GitHub!
Feel free to fork, improve, or open pull requests to contribute.

```

---

Would you like this customized with your actual GitHub repo link and image assets (banner/screenshots)? I can help host or generate those if needed.
```
