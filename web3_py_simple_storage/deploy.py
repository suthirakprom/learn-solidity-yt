from distutils.command.build import build
from solcx import compile_standard, install_solc
from web3 import Web3
import json
import os
from dotenv import load_dotenv

load_dotenv()

install_solc("0.6.0")


with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },   
    },
    solc_version = "0.6.0",
)

with open("compile_code.json", "w") as file:
    json.dump(compiled_sol, file)

bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# connecting with ganache
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chaind_id = 1337
my_address = "0xC6d20833F20cC5f0E03c3B03CF955Cb2f11E7B30"
private_key = os.getenv("PRIVATE_KEY")

# create the contract in python 
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# get the latest transaction 
nonce= w3.eth.getTransactionCount(my_address)

transaction = SimpleStorage.constructor().buildTransaction( {
    "gasPrice": w3.eth.gas_price, 
    "chainId": chaind_id, 
    "from": my_address, 
    "nonce": nonce, 
})

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# send this signed transaction 
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# working with contract:
# Contract API
# Contract Address
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Making tracsaction :
# Call = simulate making the call and getting a return value
# Transact = actually make a state change
# print(simple_storage.functions.retrieve().call())
print(simple_storage.functions.store(15).call())

store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chaind_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,
    }
)

signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)

send_store_txn = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
txn_receipt = w3.eth.wait_for_transaction_receipt(send_store_txn)