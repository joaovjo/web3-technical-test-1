# ⚡ BSC Balance Query (Consulta de Saldos na Binance Smart Chain)

Este é um projeto simples e altamente eficiente desenvolvido em Python utilizando a biblioteca **Web3.py** para interagir diretamente com a blockchain da **Binance Smart Chain (BSC)**. O script realiza a consulta em tempo real do bloco mais recente da rede, o saldo de moeda nativa (**BNB**) de uma carteira específica e o saldo do token BEP-20 **USDT** (Tether) pertencente à mesma carteira.

---

## 🚀 Principais Funcionalidades

- **Conexão de Alta Performance**: Estabelece conexão com a rede principal da BSC por meio de nós RPC HTTP públicos, contando com mecanismo automático de fallback para um nó secundário.
- **Suporte ao Consenso PoA (Proof of Authority)**: Integração e injeção do middleware `ExtraDataToPOAMiddleware` (antigo `geth_poa_middleware` nas versões anteriores do Web3.py) para contornar limites de tamanho do campo `extraData` nos blocos da BSC.
- **Normalização com Checksum**: Conversão e validação rigorosa dos endereços de carteira e do contrato para o formato **EIP-55 Checksum**, mitigando riscos de erros de formatação ou digitação.
- **Leitura do Estado da Blockchain**:
  - Consulta rápida do número do último bloco minerado/validado.
  - Consulta do saldo nativo em *Wei* e formatação amigável para *Ether/BNB*.
  - Instanciação de contrato inteligente BEP-20 de forma otimizada para consulta de saldo de tokens (USDT).

---

## 🛠️ Tecnologias e Ferramentas Utilizadas

- **Python >= 3.14**: Ambiente de execução otimizado com suporte às novidades mais recentes da linguagem.
- **[Web3.py](https://web3py.readthedocs.io/) (v7.16.0+)**: Biblioteca padrão da indústria para interação com protocolos compatíveis com EVM (Ethereum Virtual Machine).
- **[python-dotenv](https://github.com/theofidry/python-dotenv)**: Gerenciamento limpo e seguro de variáveis de ambiente.
- **[uv](https://github.com/astral-sh/uv)**: Gerenciador de pacotes e instalador em Rust ultra-rápido para garantir a consistência de dependências (`pyproject.toml` e `uv.lock`).

---

## ⚙️ Instalação e Configuração

### 1. Instalação do Gerenciador `uv`
Se você ainda não utiliza o `uv`, pode instalá-lo de maneira simples e rápida:

- **Windows (PowerShell)**:
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
- **macOS / Linux**:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

### 2. Configurar o Ambiente Virtual e Dependências
Dentro do diretório raiz do projeto, execute o comando abaixo para criar o ambiente virtual `.venv` e sincronizar todas as dependências automaticamente:

```bash
uv sync
```

### 3. Configurar as Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto baseando-se no modelo disponibilizado:

```bash
cp .env.example .env
```

Abra o arquivo `.env` gerado e defina as variáveis necessárias:
- **`RPC_URL`**: URL principal do nó RPC da BSC (Ex: `https://bsc-dataseed.binance.org/`).
- **`RPC_URL_BACKUP`**: URL secundária para fallback.
- **`WALLET_ADDRESS`**: O endereço da carteira a ser consultada (o arquivo `.env.example` fornece exemplos de carteiras conhecidas da própria Binance).
- **`USDT_CONTRACT`**: O endereço oficial do contrato inteligente do USDT na BSC (`0x55d398326f99059fF775485246999027B3197955`).

---

## 🏃‍♂️ Como Executar

Com o ambiente virtual ativado e as variáveis configuradas no `.env`, execute o script principal usando o runner do `uv`:

```bash
uv run main.py
```

*(Alternativamente, se preferir usar o ambiente virtual clássico ativado)*:
```bash
python main.py
```

### 📋 Exemplo de Saída no Terminal

```text
--- Consulta BSC ---
Bloco atual da BSC: 99880484
Saldo Nativo (BNB): 6297257.199987522725 BNB
Saldo Token (USDT): 159563372.237852164053876194 USDT
--------------------
```

---

## 🧠 Detalhes Técnicos & Boas Práticas

### 🔹 Consenso Proof of Authority (PoA) da BSC
A rede da Binance Smart Chain não utiliza Proof of Work (PoW) como a rede antiga do Ethereum, mas sim uma variação de **Proof of Authority (PoA)**. Em blocos de redes PoA, o validador insere assinaturas digitais no cabeçalho do bloco, no campo `extraData`. Isso faz com que esse campo frequentemente exceda o tamanho padrão de 32 bytes estipulado pelas regras tradicionais do Ethereum.

Sem a injeção do middleware `ExtraDataToPOAMiddleware` na camada zero da fila de middlewares da Web3:
```python
w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
```
a biblioteca levantaria uma exceção de validação (`ValidationError`), impedindo qualquer leitura da rede.

### 🔹 ABI Otimizada para Tokens (Minimal ERC-20 ABI)
Em vez de importar a ABI completa do token USDT (que possui dezenas de funções, eventos e consome dezenas de kilobytes de dados desnecessários), este script emprega uma técnica de **ABI Mínima**. Declaramos apenas o esqueleto da função de consulta de saldos:

```python
BEP20_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function",
    }
]
```
Isso é 100% compatível com a chamada `balanceOf(address)` exposta em qualquer contrato inteligente padrão ERC-20 ou BEP-20, mantendo a inicialização do contrato rápida e o código extremamente limpo.

---

## 📄 Licença

Este projeto é de caráter educacional e demonstrativo para fins de teste técnico. Fique à vontade para copiar, modificar e utilizar o código conforme as suas necessidades!
