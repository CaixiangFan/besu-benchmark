from web3 import  Web3
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

print(web3.isConnected())

print(web3.eth.blockNumber)

balance = web3.eth.getBalance("0xDd10fFef944326589562416e85f1dea35e894107")
print(web3.fromWei(balance, "ether"))