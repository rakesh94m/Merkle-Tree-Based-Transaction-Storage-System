# app.py
from flask import Flask, render_template, request, redirect, url_for
from merkle_tree_code import build_merkle_tree
from database_functions import (
    get_all_transactions, 
    insert_transaction_to_db, 
    init_db, 
    get_stored_layers,
    update_stored_layers
)
import datetime

app = Flask(__name__)

def get_tampered_path(computed_layers, stored_layers):
    tampered_hashes = []
    if not computed_layers or not stored_layers:
        return tampered_hashes

    # Go through all layers from leaves upward
    for i in range(len(computed_layers)):
        for j in range(len(computed_layers[i])):
            if computed_layers[i][j] != stored_layers[i][j]:
                # Found the first tampered leaf
                parent_index = j
                level = i
                while level < len(computed_layers):
                    # add current node
                    tampered_hashes.append(computed_layers[level][parent_index])
                    # move to parent
                    parent_index //= 2
                    level += 1
                return tampered_hashes

    return tampered_hashes


@app.route('/')
def index():
    transactions = get_all_transactions()
    tree_data = build_merkle_tree(transactions)
    merkle_root = tree_data["root"]
    
    stored_layers = get_stored_layers()
    computed_layers = tree_data["layers"]
    
    is_tampered = False
    tampered_hashes = []

    # Check for tampering only if a tree exists and the number of layers match
    if stored_layers and len(stored_layers) == len(computed_layers) and stored_layers[-1][0] != computed_layers[-1][0]:
        is_tampered = True
        tampered_hashes = get_tampered_path(computed_layers, stored_layers)
            
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return render_template('index.html', 
                           transactions=transactions, 
                           merkle_root=merkle_root, 
                           is_tampered=is_tampered,
                           original_root=get_stored_layers()[-1][0] if get_stored_layers() else None,
                           current_time=current_time,
                           merkle_tree_layers=computed_layers,
                           tampered_hashes=tampered_hashes)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    tx_id = request.form['tx_id']
    sender = request.form['sender']
    receiver = request.form['receiver']
    amount = float(request.form['amount'])
    timestamp = request.form['timestamp']
    
    insert_transaction_to_db(tx_id, sender, receiver, amount, timestamp)
    
    transactions = get_all_transactions()
    new_tree = build_merkle_tree(transactions)
    update_stored_layers(new_tree["layers"])

    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)