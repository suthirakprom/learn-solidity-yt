from brownie import FundMe, network, accounts, config
from scripts.helpful_scripts import get_account


def deploy_fund_me():
    account = get_account()

    # pass pricefeed address to fundme contract
    if network.show_active() != "development": 
        price_feed_address =  config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else: 
        price_feed_address = accounts[0]
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account}, 
        publish_source=True
    )
    print(f"Contract deployed to {fund_me.address}")

def main():
    deploy_fund_me()