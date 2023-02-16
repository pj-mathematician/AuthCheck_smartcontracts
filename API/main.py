from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
# Load data from the data.json file
with open('data.json') as f:
    data = eval(f.read())['data']
@app.route('/nft/<string:token_id>', methods=['GET'])
@cross_origin()
def get_nft(token_id):
    try:
        import pytezos
    except:
        print("pytezos installation required!")
        return
    # Connect to Tezos network
    pytezos = pytezos.using(shell="mainnet") # pytezos.using(shell="ghostnet")

    # Get the token contract and storage
    token_contract = pytezos.contract('KT1...', entry_point='get_token_metadata')
    token_storage = token_contract.storage()

    # Get the NFT metadata
    token_metadata = token_storage[token_id]

    # Get the predefined metadata
    predefined_metadata = {
        "name": "Tezos NFT",
        "description": "An NFT on the Tezos blockchain",
        "image": "https://example.com/nft.png"
    }

    # Combine the NFT metadata and predefined metadata
    nft_metadata = {**token_metadata, **predefined_metadata}

    # Return the metadata as JSON
    return jsonify(nft_metadata)


app.run(host='0.0.0.0', port=81)
