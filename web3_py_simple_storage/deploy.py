from solcx import compile_standard, install_solc
from web3 import Web3
import json


install_solc("0.6.0")


with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    print(simple_storage_file)

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
chained_id = 5777
my_address = "0xC6d20833F20cC5f0E03c3B03CF955Cb2f11E7B30"
private_key = "0x6fc0f72e1e3f285d41087565a1e97001d123094c0f6baac1c1e13c5c43d63ade"