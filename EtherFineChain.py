from flask import Flask, request, jsonify
from flask_cors import CORS
from web3 import Web3
from eth_account import Account
import os
import json
from datetime import datetime
from eth_utils import to_checksum_address  # Add at top
import requests
from eth_account import Account
import csv
import os




app = Flask(__name__)
CORS(app)

# Ganache Setup
WEB3_PROVIDER_URL = "HTTP://127.0.0.1:7545"
PRIVATE_KEY = "0x69d4f6b15f784bcf2ade6edd0ed6b3807680a6795da3850a27a3d15ac5197c23"  # Paste from Ganache 
CONTRACT_ADDRESS = "0x523B997B2134e4c4933CB74972997c884c704252"

# Load ABI from compiled contract
with open('TrafficViolationSystemABI2.json') as f:  # Save your ABI as a .json file
    CONTRACT_ABI = json.load(f)

# Web3 setup
w3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URL))
# account = Account.from_key(PRIVATE_KEY)
# sender_address = account.address


contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

# In your AllTheBest.py, add this right after setting up Web3
# This will transfer ETH from the first Ganache account to your sending account
# if w3.eth.get_balance(sender_address) < w3.to_wei(5, 'ether'):
#     first_account = w3.eth.accounts[0]
#     w3.eth.send_transaction({
#         'from': first_account,
#         'to': sender_address,
#         'value': w3.to_wei(10, 'ether')
#     })


print("Chain ID (Ganache):", w3.eth.chain_id)




def upload_to_pinata(file):
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {
        "pinata_api_key": "5d8604bfbe02dfc562b5",
        "pinata_secret_api_key": "32ca5b7048ec702217bfee9a16533370fb3f03ddc022060879a5209ddcdfa2d3"
    }
    files = {'file': (file.filename, file.stream, file.mimetype)}
    response = requests.post(url, files=files, headers=headers)
    if response.status_code == 200:
        ipfs_hash = response.json()['IpfsHash']
        return ipfs_hash
    else:
        raise Exception(f"Pinata upload failed: {response.text}")
    

@app.route('/api/process-violation-manual', methods=['POST'])
def process_violation_manual():
    try:
        import time  # ADD this import at the top
        start_total = time.time()  # ✅ Total start
        vehicle_id = request.form['vehicle_id']
        violation_type = request.form['violation_type']
        location = request.form.get('location', '')
        camera_id = request.form.get('camera_id', '')
        owner_address = request.form['owner_address']

        # Handle uploaded file
        # file = request.files.get('violation_image')
        # image_hash = f"mocked_hash_{datetime.now().strftime('%H%M%S')}"
        # pinata_url = f"https://gateway.pinata.cloud/ipfs/{image_hash}"

        # Step 2: Extract and verify private key
        owner_private_key = request.form.get('owner_private_key')
        if not owner_private_key:
            return jsonify({'error': 'Missing private key'}), 400

        try:
            from eth_account import Account
            owner_account = Account.from_key(owner_private_key)
            owner_address = owner_account.address
        except Exception as e:
            return jsonify({'error': f'Invalid private key: {str(e)}'}), 400

      

        file = request.files.get('violation_image')
        if not file:
            return jsonify({'error': 'Image evidence is required'}), 400

        # Upload to IPFS via Pinata
        try:
            start_upload = time.time()  # ✅ Start Pinata upload timer
            image_hash = upload_to_pinata(file)
            end_upload = time.time()    # ✅ End Pinata upload timer
            pinata_upload_time = (end_upload - start_upload) * 1000  # in ms
        except Exception as upload_error:
            return jsonify({'error': f"IPFS upload failed: {str(upload_error)}"}), 500

        pinata_url = f"https://gateway.pinata.cloud/ipfs/{image_hash}"


        # Convert penalty (example)
        penalty_eth = {'Speeding': 0.05, 'Red Light': 0.03, 'No Helmet': 0.01}.get(violation_type, 0.5)
        penalty_wei = w3.to_wei(penalty_eth, 'ether')


        try:
            owner_address = to_checksum_address(request.form['owner_address'])
        except Exception:
            return jsonify({'error': 'Invalid Ethereum address format'}), 400

        # Prepare transaction
        # nonce = w3.eth.get_transaction_count(sender_address)
        # txn = contract.functions.addViolation(
        #     vehicle_id, "T123", violation_type, image_hash,
        #     int(datetime.now().timestamp()), location, camera_id,
        #     penalty_wei, owner_address
        # ).build_transaction({
        #     'from': sender_address,
        #     'nonce': nonce,
        #     'gas': 3000000,
        #     'gasPrice': w3.to_wei('20', 'gwei')
        # })

        # print("Sender:", sender_address)
        # print("Owner (form):", owner_address)



# Step 5: Build and send transaction from violator's account
        txn = contract.functions.addViolation(
            vehicle_id, "T123", violation_type, image_hash,
            int(datetime.now().timestamp()), location, camera_id, owner_address
        ).build_transaction({
            'from': owner_address,
            'value': penalty_wei,
            'nonce': w3.eth.get_transaction_count(owner_address),
            'gas': 800000,
            'gasPrice': w3.to_wei('20', 'gwei'),
            'chainId': 1337  # Ganache's chain ID
        })


        signed_txn = w3.eth.account.sign_transaction(txn, private_key=owner_private_key)
        raw_tx = getattr(signed_txn, 'rawTransaction', getattr(signed_txn, 'raw_transaction', None))
        if raw_tx is None:
            return jsonify({'error': 'Could not extract raw transaction from signed_txn'}), 500


        start_tx = time.time()  # ✅ Start transaction timer
        tx_hash = w3.eth.send_raw_transaction(raw_tx)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        end_tx = time.time()  # ✅ End transaction timer
        tx_latency = (end_tx - start_tx) * 1000  # in ms
        total_time = (end_tx - start_total) * 1000  # in ms


        if receipt.status != 1:
            return jsonify({'error': 'Transaction reverted on-chain'}), 500

        # Prepare log entry
        csv_file = "results_log.csv"
        log_headers = [
            "Certificate", "Tx Hash", "Pinata Upload (ms)",
            "Transaction Latency (ms)", "Total Time (ms)", "Gas Used"
        ]

        log_data = [
            file.filename, tx_hash.hex(), round(pinata_upload_time, 2),
            round(tx_latency, 2), round(total_time, 2), receipt.gasUsed
        ]

        # Write header only once
        file_exists = os.path.exists(csv_file)
        with open(csv_file, mode='a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(log_headers)
            writer.writerow(log_data)


        return jsonify({
            'success': True,
            'tx_hash': tx_hash.hex(),
            'image_hash': image_hash,
            'pinata_url': pinata_url,
            'penalty_amount': penalty_eth,
            'owner_address': owner_address,
            'pinata_upload_time_ms': round(pinata_upload_time, 2),
            'transaction_latency_ms': round(tx_latency, 2),
            'total_latency_ms': round(total_time, 2),
            'gas_used': receipt.gasUsed
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/api/results-table', methods=['GET'])
def get_results_table():
    try:
        csv_file = "results_log.csv"
        if not os.path.exists(csv_file):
            return jsonify({'error': 'Results file not found'}), 404

        with open(csv_file, newline='') as f:
            reader = csv.reader(f)
            rows = list(reader)

        if len(rows) <= 1:
            return jsonify({'message': 'Not enough records yet', 'rows': rows}), 200

        return jsonify({'rows': rows}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
