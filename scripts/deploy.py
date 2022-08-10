from brownie import FundMe, network, config, MockV3Aggregator
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_fund_me():
    account = get_account()
    # pass the price feed address to our fundme contracts

    # if we are on persistante network like kovan, use the associated address
    # otherwise, deploy mocks
    # if network.show_active() != "development":
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        # price_feed_adress = "0x9326BFA02ADD2366b30bacB125260Af641031331"
        # we can get this address from brownie config section
        price_feed_adress = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    # if we are on development chain
    # let's deploy this mocks
    else:
        # call mock from helpful script
        deploy_mocks()
        price_feed_adress = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_adress,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get(
            "verify"
        ),  # .get for if we forget to add verify
    )
    print(f"Contract Deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
