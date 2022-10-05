from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fund_me
from brownie import accounts, FundMe, network, exceptions
import pytest


def test_can_fund_and_withdraw():
    """in this section we declare account, deploy contract and set entrance fee
    after we assert the address of that mapping equal to the value after and before withdraw"""
    # arrange
    account = get_account()

    # act
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee() + 100
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)

    # assert
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee

    tx_2 = fund_me.withdraw({"from": account})
    tx_2.wait(1)

    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    """in this section we want to know a different account can withdraw
    or not?!"""
    if (
        network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS
    ):  # means that on live network
        pytest.skip("only for local testing")

    # arrange
    bad_actor = accounts.add()  # generate a random account
    fund_me = deploy_fund_me()

    fund_me.withdraw({"from": bad_actor})
    with pytest.raises(exceptions.VirtualMachineError):
        # if this reverts with virtual machine error, that's good
        fund_me.withdraw({"from": bad_actor})
