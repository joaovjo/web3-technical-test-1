from web3 import Web3, HTTPProvider
from dotenv import load_dotenv

def main():
    w3 = Web3(HTTPProvider("https://bsc-dataseed.binance.org/"))