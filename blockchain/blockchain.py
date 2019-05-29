blockchain = []
open_transactions = []
owner = 'Pedro'
genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': []
}
blockchain.append(genesis_block)

def hash_block(block):
    return '-'.join([str(block[key]) for key in block])

def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    print(hashed_block)
    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': open_transactions
    }
    blockchain.append(block)


def verify_chain():
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False
    return True


def get_last_blockchain_value():
    """
    Returns last value from blockchain
    :return: list
    """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(recipient, sender=owner, amount=1.0):
    """
    Adds a value to the blockchain list
    :param transaction_amount:
    :param last_transaction:
    :return:
    """
    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }
    open_transactions.append(transaction)

def get_transaction_value():
    tx_recipient = input('Escriba el beneficiario de la transacción: ')
    tx_amount = float(input('El monto de su transacción, por favor: '))
    return tx_recipient, tx_amount

def get_user_choice():
    return input('Su elección: ')

def print_blockchain_elements():
    for block in blockchain:
        print(block)


waiting_for_input = True

while waiting_for_input:
    print('Elija por favor: ')
    print('1: Agregue un nuevo valor de la transacción')
    print('2: Minar bloque')
    print('3: Muestre los bloques de la cadena')
    print('h: Manipular la blockchain')
    print('s: Salir')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        add_transaction(recipient, amount=amount)
        print(open_transactions)
    elif user_choice == '2':
        mine_block()
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash': '',
                'index': 0,
                'transactions': [{'sender': 'Ximena', 'recipient': 'Pedro', 'amount': 10}]
            }
    elif user_choice == 's':
        waiting_for_input = False
    else:
        print('Opción inválida, elija una opción de la lista')

    if not verify_chain():
        print('Blockchain inválida')
        break
else:
    print('El usuario ha finalizado las transacciones')

