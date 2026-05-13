from flask import Flask, jsonify
import os
import json
import base64
from Crypto.Cipher import AES

import hmac
import hashlib

app = Flask(__name__)

#Last two digits of Student ID 11762337 is 37 (Sunny's EUID)

SECRET_KEY = b"super_secret_32_byte_key_for_aes" #HARD CODED SECRET KEY

DATA = { #payload data - to be sent
    "location": "Denton, TX",
    "temperature_c": 10,
    "temperature_f": 50,
    "condition": "Partly Cloudy",
    "humidity_percent": 37,
}

#STEP 2

# @app.get("/weather")
# def weather():
#     plaintext = json.dumps(DATA).encode('utf-8') #stringifying json
#     nonce = os.urandom(8) #random nonce creating
#     cipher = AES.new(SECRET_KEY, AES.MODE_CTR, nonce=nonce)
#     ciphertext = cipher.encrypt(plaintext) #encryping the plaintext to get ciphertext
    

#     return jsonify({
#         "nonce": base64.b64encode(nonce).decode('utf-8'),
#         "ciphertext": base64.b64encode(ciphertext).decode('utf-8')
#     })





#STEP 3

# @app.get("/weather")
# def weather():
#     payload_str = json.dumps(DATA)
#     payload_bytes = payload_str.encode('utf-8') #cnverting payload str to bytes
    
#     mac_tag = hmac.new(SECRET_KEY, payload_bytes, hashlib.sha256).hexdigest() #creating tag out of payload
    

#     return jsonify({
#         "payload": payload_str,
#         "mac": mac_tag
#     })



#Step 4


@app.get("/weather")
def weather():
    plaintext = json.dumps(DATA).encode("utf-8") #stringifying the json

    # 12-byte random nonce is standard for GCM
    nonce = os.urandom(12)

    cipher = AES.new(SECRET_KEY, AES.MODE_GCM, nonce=nonce) #creating cipher
    ciphertext, tag = cipher.encrypt_and_digest(plaintext) #creating tag and ciphertext to be sent

    #sending json response containing the created nonce, ciphertext and tag
    return jsonify({
        "nonce": base64.b64encode(nonce).decode("utf-8"),
        "ciphertext": base64.b64encode(ciphertext).decode("utf-8"),
        "tag": base64.b64encode(tag).decode("utf-8")
    })



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5037, debug=True) #running on port 5037
