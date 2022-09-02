import os
from solcx import compile_standard, install_solc
import json
from web3 import Web3
from dotenv import load_dotenv
from brownie import accounts, network, config, VendingMachine

# run: brownie compile
# run: brownie run scripts/deploy.py


def main():
    deploy_FundMe()


def getAccount():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.load("rodrigolb")


def deploy_VendingMachine2():
    account = getAccount()
    machine = VendingMachine.deploy({"from": account})
    burgers = machine.getVendingMachineDonutsBalance()
    print(burgers)
    restock = machine.restock(10, {"from": account})
    print(restock)
    burgers = machine.getVendingMachineDonutsBalance()
    print(burgers)


def deploy_FundMe():
    install_solc("0.6.0")
    load_dotenv()

    with open("D:\Leassons and Assignments\Brownie1\contracts\FundMe.sol", "r") as file:
        FundMe = file.read()

    # Compile our Soldity
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"FundMe.sol": {"content": FundMe}},
            "settings": {
                "outputSelection": {
                    "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                }
            },
        },
        solc_version="0.6.0",
    )

    with open("compiled_sol", "w") as file:
        json.dump(compiled_sol, file)

    # get bytecode
    bytecode = compiled_sol["contracts"]["FundMe.sol"]["FundMe"]["evm"]["bytecode"][
        "object"
    ]

    # get abi
    abi = compiled_sol["contracts"]["FundMe.sol"]["FundMe"]["abi"]

    # for connecting to Ganache
    w3 = Web3(
        Web3.HTTPProvider(
            "https://goerli.infura.io/v3/141d722c9b834dc9a38a0bf0dd40cfe8"
        )
    )
    chain_id = 5
    my_address = "0x44818e00A3E71582858425707746fb7DDFab927e"
    # ! WARNING !
    private_key = os.getenv("GOERLI_PRIVATE_KEY")

    # create the contract in Python
    FundMe = w3.eth.contract(abi=abi, bytecode=bytecode)
    print(FundMe)
    # get the latest transaction
    nonce = w3.eth.getTransactionCount(my_address)
    # build a transaction
    transaction = FundMe.constructor().buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "chainId": chain_id,
            "from": my_address,
            "nonce": nonce,
        }
    )
    print(transaction)
    # sign transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
    # send transaction
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    # wait for block confirmation to happen
    print("generated receipt:")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)


def deploy_VendingMachine():

    install_solc("0.6.0")
    load_dotenv()

    with open(
        "D:\Leassons and Assignments\Brownie1\contracts\VendingMachine.sol", "r"
    ) as file:
        Vending_machine = file.read()

    # Compile our Soldity
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"VendingMachine.sol": {"content": Vending_machine}},
            "settings": {
                "outputSelection": {
                    "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                }
            },
        },
        solc_version="0.6.0",
    )

    with open("compiled_sol", "w") as file:
        json.dump(compiled_sol, file)

    # get bytecode
    bytecode = compiled_sol["contracts"]["VendingMachine.sol"]["VendingMachine"]["evm"][
        "bytecode"
    ]["object"]

    # get abi
    abi = compiled_sol["contracts"]["VendingMachine.sol"]["VendingMachine"]["abi"]

    # for connecting to Ganache
    w3 = Web3(
        Web3.HTTPProvider(
            "https://goerli.infura.io/v3/141d722c9b834dc9a38a0bf0dd40cfe8"
        )
    )
    chain_id = 5
    my_address = "0x44818e00A3E71582858425707746fb7DDFab927e"
    # ! WARNING !
    private_key = os.getenv("GOERLI_PRIVATE_KEY")

    # create the contract in Python
    Vending_Machine = w3.eth.contract(abi=abi, bytecode=bytecode)
    print(Vending_Machine)
    # get the latest transaction
    nonce = w3.eth.getTransactionCount(my_address)
    # build a transaction
    transaction = Vending_Machine.constructor().buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "chainId": chain_id,
            "from": my_address,
            "nonce": nonce,
        }
    )
    print(transaction)
    # sign transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
    # send transaction
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    # wait for block confirmation to happen
    print("generated receipt:")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    # Interact with the contract
    vendingMachine = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

    getBalance = (
        vendingMachine.functions.getVendingMachineDonutsBalance().buildTransaction(
            {
                "gasPrice": w3.eth.gas_price,
                "chainId": chain_id,
                "from": my_address,
                "nonce": nonce + 1,
            }
        )
    )
    print(getBalance)
    # sign
    signed_getBalance_txn = w3.eth.account.sign_transaction(getBalance, private_key)
    # send
    tx_balance_hash = w3.eth.send_raw_transaction(signed_getBalance_txn.rawTransaction)
    # wait
    tx_balance_receipt = w3.eth.wait_for_transaction_receipt(tx_balance_hash)
    print(tx_balance_receipt)
