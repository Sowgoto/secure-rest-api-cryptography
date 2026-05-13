from flask import Flask, jsonify
import os
import json
import base64
from Crypto.Cipher import AES

import hmac
import hashlib

app = Flask(__name__)

#Last two digits of Student ID 11762337 --- so for fake server its going to be 38

SECRET_KEY = b"attacker_wrong_32_byte_secret_key!" #HARD CODED SECRET KEY for attacker

#Payload
DATA = {
    "location": "Denton, TX",
    "temperature_c": 10,
    "temperature_f": 50,
    "condition": "Partly Cloudy",
    "humidity_percent": 38,
}

#STEP 2

# @app.get("/weather")
# def weather():
#     plaintext = json.dumps(DATA).encode('utf-8')
#     nonce = os.urandom(8)
#     cipher = AES.new(SECRET_KEY, AES.MODE_CTR, nonce=nonce)
#     ciphertext = cipher.encrypt(plaintext)
    

#     return jsonify({
#         "nonce": base64.b64encode(nonce).decode('utf-8'),
#         "ciphertext": base64.b64encode(ciphertext).decode('utf-8')
#     })


#STEP 3
@app.get("/weather")
def weather():
    #Converting payload into string
    payload_str = json.dumps(DATA)
    
    #Reading the stored tag
    with open("tag.txt", "r", encoding="utf-8") as f:
        intercepted_tag = f.read().strip()

    #json response containing the payload and tag
    return jsonify({
        "payload": payload_str,
        "mac": intercepted_tag
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5038, debug=True) #fake server running on port 5038
