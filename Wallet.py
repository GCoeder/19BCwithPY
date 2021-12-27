# Import dependencies
import subprocess
import json
from dotenv import load_dotenv
from bit import PrivateKeyTestnet
from bit.network import NetworkAPI
import os 
from web3 import Account, Web3
# Load and set environment variables
load_dotenv()
mnemonic=os.getenv("mnemonic")

# Import constants.py and necessary functions from bit and web3
# from bit import wif_to_key
from constants import BTC, ETH, BTCTEST 
 
 
# Create a function called `derive_wallets`
def derive_wallets(coin):
    command = f'~/php ./derive -g --mnemonic="fiscal behave wealth immune spawn position pigeon exile snow tomato try member\
" --cols=path,address,privkey,pubkey --format=json --coin={coin}'

    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)

def priv_key_to_account(coin, priv_key):
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    if coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)    
        
# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
def create_tx(coin, account, recipient, amount, w3):
    if coin == ETH:
        gasEstimate = w3.eth.estimateGas(
            {"from": account.address, "to": recipient, "value": amount}
        )
        return {
            "from": account.address,
            "to": recipient,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address),
        }
    elif coin ==BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(recipient, amount, BTC)])


# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_tx(coin, account, recipient, amount, w3):
    if coin == ETH:
        tx = create_tx(coin, account, recipient, amount, w3)
        signed_tx = account.sign_transaction(tx)
        result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(result.hex())
        return result.hex()
    elif coin == BTCTEST:
        tx = create_tx(coin, account, recipient, amount, w3)
        signed_tx = account.sign_transaction(tx)
        result = NetworkAPI.broadcast_tx_testnet(signed_tx)
        return result

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

coins = {BTCTEST : derive_wallets(BTCTEST), ETH : derive_wallets(ETH)}

btc_test_key = coins[BTCTEST][0]['privkey']
eth_test_key = coins[ETH][0]['privkey']

btc_account = priv_key_to_account(BTCTEST, btc_test_key)
eth_account = priv_key_to_account(ETH, eth_test_key)

print(eth_account)

print(eth_test_key)
