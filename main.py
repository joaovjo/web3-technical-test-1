from web3 import Web3, HTTPProvider
from web3.middleware import ExtraDataToPOAMiddleware
from dotenv import load_dotenv
import os 

# Carregar .env para obter as variáveis de ambiente
load_dotenv()

# Setar as envs necessárias
RPC_URL = os.getenv("RPC_URL") or os.getenv("RPC_URL_BACKUP")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
USDT_CONTRACT = os.getenv("USDT_CONTRACT")

# API é o contrato em nível de código-fonte, ABI é o contrato em nível de binário
# ABI mínima necessária para consultar saldos de tokens ERC-20/BEP-20
BEP20_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function",
    }
]


def main():
    # Estabelecer conexão com o Nó RPC via HTTPProvider
    w3 = Web3(HTTPProvider(RPC_URL))

    if not w3.is_connected():
        print("Erro: Não foi possível conectar à BSC.")
        return

    # Por causa do mecanismo de consenso da BSC (Proof of Authority), precisamos injetar um middleware específico para lidar com os campos extras nos blocos, se não fizer isso vai dar erro de "Extra Data Too Long" porque quebra o limite máximo permitido pelo Ethereum.

    # A partir da v7 o geth_poa_middleware foi renomeado para ExtraDataToPOAMiddleware para maior clareza
    # Link da documentação https://web3py.readthedocs.io/en/latest/migration.html#middleware-renaming-and-removals

    w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

    # Converter endereços para formato Checksum (Exigência de segurança do Web3.py)
    wallet = w3.to_checksum_address(WALLET_ADDRESS)
    usdt_address = w3.to_checksum_address(USDT_CONTRACT)

    print("--- Consulta BSC ---")

    # Consultar o Bloco Atual
    bloco_atual = w3.eth.block_number
    print(f"Bloco atual da BSC: {bloco_atual}")

    # Consultar saldo em wei (menor unidade no Ethereum/BSC, equivalente ao satoshi do Bitcoin)
    saldo_wei = w3.eth.get_balance(wallet)

    # Converter saldo nativo (BNB)
    saldo_bnb = w3.from_wei(saldo_wei, "ether")
    print(f"Saldo Nativo (BNB): {saldo_bnb} BNB")

    # Consultar Saldo de Token (USDT)
    # Criamos a instância do contrato usando o endereço e a ABI
    contrato_usdt = w3.eth.contract(address=usdt_address, abi=BEP20_ABI)

    # Chamamos a função 'balanceOf' lendo diretamente da blockchain (.call())
    saldo_usdt_bruto = contrato_usdt.functions.balanceOf(wallet).call()

    # O USDT na BSC também utiliza 18 casas decimais
    saldo_usdt = w3.from_wei(saldo_usdt_bruto, "ether")
    print(f"Saldo Token (USDT): {saldo_usdt} USDT")
    print("--------------------")


if __name__ == "__main__":
    main()
