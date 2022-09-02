from brownie import accounts, VendingMachine

# run: bronie test -s


def test_deploy():
    # arrange
    account = accounts.load("rodrigolb")
    # act
    vendingMachine = VendingMachine.deploy({"from": account})
    burgers_balance = vendingMachine.getVendingMachineDonutsBalance()
    expected = 100
    # assert
    assert burgers_balance == expected


# brownie networks list
#(development networks are temporary)

