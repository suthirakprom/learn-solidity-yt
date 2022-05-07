from brownie import FundMe
from scripts.helpful_scripts import get_account


def deploy_fund_me():
    account = get_account()

    # pass pricefeed address to fundme contract
    fund_me = FundMe.deploy(
        "0x9246f813c1C36D9B816BAb34e7366fD3992d1E5f",
        {"from": account}, 
        publish_source=True
    )
    print(f"Contract deployed to {fund_me.address}")

def main():
    deploy_fund_me()