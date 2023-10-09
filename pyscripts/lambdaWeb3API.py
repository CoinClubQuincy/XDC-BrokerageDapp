import sha3
from web3.auto import w3
from web3 import Web3, AsyncWeb3
from web3 import Web3, EthereumTesterProvider
from web3.middleware import construct_sign_and_send_raw_middleware
from eth_account import Account
import os

class localSeedStoragetest:
    def create_user(address,seed,index):
        user = {
            "address": address,
            "seed": seed,
            "index": [],
        }

class executeWeb3:
    w3 = None
    sender_address = None

    erc20_contract_abi = [
    {'constant': True,'inputs': [],'name': 'name','outputs': [{'name': '', 'type': 'string'}],'payable': False,'type': 'function'},
    {'constant': True,'inputs': [],'name': 'symbol','outputs': [{'name': '', 'type': 'string'}],'payable': False,'type': 'function'},
    {'constant': True,'inputs': [],'name': 'decimals','outputs': [{'name': '', 'type': 'uint8'}],'payable': False,'type': 'function'},
    {'constant': False,'inputs': [{'name': '_spender', 'type': 'address'}, {'name': '_value', 'type': 'uint256'}],'name': 'approve','outputs': [{'name': 'success', 'type': 'bool'}],'payable': False,'type': 'function'},
    {'constant': True,'inputs': [{'name': '_owner', 'type': 'address'}, {'name': '_spender', 'type': 'address'}],'name': 'allowance','outputs': [{'name': 'remaining', 'type': 'uint256'}],'payable': False,'type': 'function'},
    {'constant': False,'inputs': [{'name': '_to', 'type': 'address'}, {'name': '_value', 'type': 'uint256'}],'name': 'transfer','outputs': [{'name': 'success', 'type': 'bool'}],'payable': False,'type': 'function'},
    {'constant': False,'inputs': [{'name': '_spender', 'type': 'address'}, {'name': '_value', 'type': 'uint256'}, {'name': '_extraData', 'type': 'bytes'}],'name': 'approveAndCall','outputs': [{'name': 'success', 'type': 'bool'}],'payable': False,'type': 'function'},
    {'constant': True,'inputs': [{'name': '_owner', 'type': 'address'}],'name': 'balanceOf','outputs': [{'name': 'balance', 'type': 'uint256'}],'payable': False,'type': 'function'},
    {'constant': False,'inputs': [{'name': '_from', 'type': 'address'}, {'name': '_to', 'type': 'address'}, {'name': '_value', 'type': 'uint256'}],'name': 'transferFrom','outputs': [{'name': 'success', 'type': 'bool'}],'payable': False,'type': 'function'},
    {'constant': False,'inputs': [{'name': '_to', 'type': 'address'}, {'name': '_value', 'type': 'uint256'}, {'name': '_extraData', 'type': 'bytes'}],'name': 'transferAndCall','outputs': [{'name': 'success', 'type': 'bool'}],'payable': False,'type': 'function'},
    {'inputs': [{'name': '_initialAmount', 'type': 'uint256'}, {'name': '_tokenName', 'type': 'string'}, {'name': '_decimalUnits', 'type': 'uint8'}, {'name': '_tokenSymbol', 'type': 'string'}],'type': 'constructor'},
    {'anonymous': False,'inputs': [{'indexed': True, 'name': '_from', 'type': 'address'}, {'indexed': True, 'name': '_to', 'type': 'address'}, {'indexed': False, 'name': '_value', 'type': 'uint256'}],'name': 'Transfer','type': 'event'},
    {'anonymous': False,'inputs': [{'indexed': True, 'name': '_owner', 'type': 'address'}, {'indexed': True, 'name': '_spender', 'type': 'address'}, {'indexed': False, 'name': '_value', 'type': 'uint256'}],'name': 'Approval','type': 'event'}
    ]
    erc1155_contract_abi = [
    {"constant": True,"inputs": [{"name": "account","type": "address"},{"name": "id","type": "uint256"}],"name": "balanceOf","outputs": [{"name": "","type": "uint256"}],"payable": False,"stateMutability": "view","type": "function"},
    {"constant": False,"inputs": [{"name": "to","type": "address"},{"name": "id","type": "uint256"},{"name": "amount","type": "uint256"},{"name": "data","type": "bytes"}],"name": "safeTransferFrom","outputs": [],"payable": False,"stateMutability": "nonpayable","type": "function"},
    {"constant": True,"inputs": [{"name": "owner","type": "address"}],"name": "isApprovedForAll","outputs": [{"name": "","type": "bool"}],"payable": False,"stateMutability": "view","type": "function"},
    {"constant": False,"inputs": [{"name": "operator","type": "address"},{"name": "approved","type": "bool"}],"name": "setApprovalForAll","outputs": [],"payable": False,"stateMutability": "nonpayable","type": "function"},
    {"anonymous": False,"inputs": [{"indexed": True,"name": "operator","type": "address"},{"indexed": True,"name": "from","type": "address"},{"indexed": True,"name": "to","type": "address"},{"indexed": False,"name": "id","type": "uint256"},{"indexed": False,"name": "amount","type": "uint256"}],"name": "TransferSingle","type": "event"},
    {"anonymous": False,"inputs": [{"indexed": True,"name": "operator","type": "address"},{"indexed": True,"name": "from","type": "address"},{"indexed": True,"name": "to","type": "address"},{"indexed": False,"name": "ids","type": "uint256[]"},{"indexed": False,"name": "amounts","type": "uint256[]"}],"name": "TransferBatch","type": "event"},
    {"anonymous": False,"inputs": [{"indexed": True,"name": "owner","type": "address"},{"indexed": True,"name": "operator","type": "address"},{"indexed": False,"name": "approved","type": "bool"}],"name": "ApprovalForAll","type": "event"}
    ]

    def __init__(self,_network,_sender_address):
        network = _network
        sender_address = _sender_address

        w3 = Web3(Web3.HTTPProvider(network))
        Account.enable_unaudited_hdwallet_features()

        self.w3 = w3
        print("Joining: [ %s ] network, with Address: %s IS CONNECTED %s" % (network,sender_address,self.w3.is_connected()))


    def balance(self,address):
        balance = self.w3.eth.get_balance(address)
        return balance

    def _formatToFloat(self,number):
        formatted_number = number / 1000000000000000000
        return formatted_number

    def _formatToBigInt(self,number):
        formatted_number = number * 1000000000000000000
        return formatted_number

    def seed_to_private_key(self,seed):
        account = Account.from_mnemonic(seed)
        private_key_hex = account.key.hex()
        return private_key_hex

    def send(self,amount,sendTo,privateKey):
        userSelf = self.w3.eth.account.from_key(privateKey)

        self.w3.middleware_onion.add(construct_sign_and_send_raw_middleware(userSelf))
     
        transaction = {
            "from": userSelf.address,
            "to": sendTo,
            "value": amount,
            "gas": 21000, 
            "gasPrice": 25,
        }

        tx_hash = self.w3.eth.send_transaction(transaction)

        tx = w3.eth.get_transaction(tx_hash)
        return tx_hash

    def sendXRC20(self, erc20_contract_address, amount, receiver_address, private_key):
        erc20_contract = self.w3.eth.contract(address=erc20_contract_address, abi=self.erc20_contract_abi)
        sender_address = self.w3.eth.account.from_key(private_key).address

        print("Balance before sending:", self.balanceXRC20(erc20_contract_address, receiver_address))

        transaction = erc20_contract.functions.transfer(receiver_address, amount)

        signed_transaction = self.w3.eth.account.sign_transaction(
            transaction.build_transaction({
                'gas': 200000,
                'gasPrice': 25,  
                'nonce': self.w3.eth.get_transaction_count(sender_address),
            }),
            private_key=private_key,
        )
        tx_hash = self.w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
        self.w3.eth.wait_for_transaction_receipt(tx_hash)

        print("Balance after sending:", self.balanceXRC20(erc20_contract_address, receiver_address))

        return tx_hash.hex()


    def balanceXRC20(self, erc20_contract_address, address_to_check):
        erc20_contract = self.w3.eth.contract(address=w3.to_checksum_address(erc20_contract_address), abi=self.erc20_contract_abi)
        symbol = erc20_contract.functions.symbol().call()
        decimals = erc20_contract.functions.decimals().call()
        name = erc20_contract.functions.name().call()
        #totalSupply = erc20_contract.functions.totalSupply().call() / 10**decimals

        balance = erc20_contract.functions.balanceOf(address_to_check).call() / 10**decimals
        return (name,symbol,balance,decimals)

    def sendERC1155(self, erc1155_contract_address, token_id, amount, receiver_address, private_key):
        erc1155_contract = self.w3.eth.contract(address=erc1155_contract_address, abi=self.erc1155_contract_abi)
        sender_address = self.w3.eth.account.from_key(private_key).address

        print("Balance before sending:", self.balanceERC1155(erc1155_contract_address, token_id, receiver_address))

        transaction = erc1155_contract.functions.safeTransferFrom(sender_address, receiver_address, token_id, amount, b"")
        
        nonce = self.w3.eth.get_transaction_count(sender_address)
        gas_price = self.w3.toWei(25, 'gwei')
        gas_limit = 200000

        transaction_dict = {
            'gas': gas_limit,
            'gasPrice': gas_price,
            'nonce': nonce,
            'chainId': self.chain_id
        }

        signed_transaction = self.w3.eth.account.sign_transaction(
            transaction.buildTransaction(transaction_dict),
            private_key=private_key,
        )
        
        tx_hash = self.w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
        self.w3.eth.wait_for_transaction_receipt(tx_hash)

        print("Balance after sending:", self.balanceERC1155(erc1155_contract_address, token_id, receiver_address))

        return tx_hash.hex()


    def balanceXRC1155(self, contract_address, address_to_check, token_id):
        erc1155_contract = self.w3.eth.contract(address=contract_address, abi=self.erc1155_contract_abi)

        balance = erc1155_contract.functions.balanceOf(address_to_check, token_id).call()
        print(f"Balance of Token ID {token_id} for {address_to_check}: {balance}")
        return balance

    def sendERC721(self, erc721_contract_address, token_id, receiver_address, private_key):
        erc721_contract = self.w3.eth.contract(address=erc721_contract_address, abi=self.erc721_contract_abi)
        sender_address = self.w3.eth.account.from_key(private_key).address

        print("Balance before sending:", self.balanceERC721(erc721_contract_address, token_id, receiver_address))

        transaction = erc721_contract.functions.safeTransferFrom(sender_address, receiver_address, token_id)
        
        nonce = self.w3.eth.get_transaction_count(sender_address)
        gas_price = self.w3.toWei(25, 'gwei')
        gas_limit = 200000

        transaction_dict = {
            'gas': gas_limit,
            'gasPrice': gas_price,
            'nonce': nonce,
            'chainId': self.chain_id
        }

        signed_transaction = self.w3.eth.account.sign_transaction(
            transaction.buildTransaction(transaction_dict),
            private_key=private_key,
        )
        
        tx_hash = self.w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
        self.w3.eth.wait_for_transaction_receipt(tx_hash)

        print("Balance after sending:", self.balanceERC721(erc721_contract_address, token_id, receiver_address))

        return tx_hash.hex()

    def balanceERC721(self, erc721_contract_address, token_id, address_to_check):
        erc721_contract = self.w3.eth.contract(address=erc721_contract_address, abi=self.erc721_contract_abi)

        balance = erc721_contract.functions.balanceOf(address_to_check, token_id).call()
        print(f"Balance of Token ID {token_id} for {address_to_check}: {balance}")
        return balance

#####################################
    def call_contract_function(url,function_name, function_params,seed):
        aws = AWS()
        contract_address, contract_abi = aws.getCIML(url)
        contract = self.w3.eth.contract(address=contract_address, abi=contract_abi)

        if function_name not in contract.functions:
            raise ValueError(f"Function '{function_name}' not found in contract ABI")

        contract_function = getattr(contract.functions, function_name)

        transaction = contract_function(*function_params).buildTransaction({
            'gas': 2000000,  
            'gasPrice': 25,  
            'nonce': web3.eth.getTransactionCount(sender_address),
        })


        signed_transaction = web3.eth.account.signTransaction(transaction, private_key=sender_private_key)

        transaction_hash = web3.eth.sendRawTransaction(signed_transaction.rawTransaction)

        #receipt = web3.eth.waitForTransactionReceipt(transaction_hash)

        return transaction_hash
        print("call Address: %s ABI: %s to %s", (address,abi))


class parseJSON:
    def parse_objects(self,json_objects):
        views = []
        sends = []
        contracts = []

        for obj in json_objects:
            obj_type = obj.get("type")
            obj_call = obj.get("call")

            if obj_type == "View":
                address = obj_call.get("address", "")
                tokens = obj_call.get("tokens", [])
                nft = obj_call.get("nft", [])
                views.append({"address": address, "tokens": tokens, "nft": nft})

            elif obj_type == "Send":
                asset = obj_call.get("asset", "")
                send_to = obj_call.get("send_to", "")
                amount = obj_call.get("amount", [])
                id_list = obj_call.get("id", [])
                sends.append({"asset": asset, "send_to": send_to, "amount": amount, "id": id_list})

            elif obj_type == "Contract":
                ciml = obj_call.get("CIML", "")
                function = obj_call.get("function", "")
                call_list = obj_call.get("call", [])
                contracts.append({"CIML": ciml, "function": function, "call": call_list})

        return views, sends, contracts
