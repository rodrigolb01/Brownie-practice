# reads an already deploy contract
# 0 for first deployment
# -1 for latest deployment

from brownie import VendingMachine, accounts, config


def read_contract():
    vending_machine = VendingMachine[-1]
    print(vending_machine.getVendingMachineDonutsBalance())


def main():
    read_contract()
