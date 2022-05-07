from brownie import accounts

def deploy_simple_storage():
    account = accounts.load("freecodecamp-account")
    print(account)

def main():
    deploy_simple_storage()