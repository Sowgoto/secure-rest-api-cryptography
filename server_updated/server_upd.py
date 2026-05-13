from flask import Flask, jsonify, request
from pathlib import Path
import json
import base64

from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
 
app = Flask(__name__) #flask server creation

DATA = { #json data to be sent, aka. payload
    "location": "Denton, TX",
    "temperature_c": 10,
    "temperature_f": 50,
    "condition": "Partly Cloudy",
    "humidity_percent": 37,
}




SERVER_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SERVER_DIR.parent

KEY_DIR = PROJECT_DIR / "keygen" #folder containing the public key
CERT_DIR = PROJECT_DIR / "server_updated"  #folder containing the certificates

PUBLIC_KEY_PATH = KEY_DIR / "public.key"
SECRET_KEY_PATH = KEY_DIR / "secret.key"
CERT_PATH = CERT_DIR / "pk.cert"


SERVER_PUBLIC_KEY_BYTES = PUBLIC_KEY_PATH.read_bytes()
SERVER_PRIVATE_KEY = RSA.import_key(SECRET_KEY_PATH.read_bytes()) #importing private key of server
PK_CERT = json.loads(CERT_PATH.read_text(encoding="utf-8")) #loading certificate





#API to send server's public key and the CA signed certificate
@app.get("/server-identity")
def server_identity():
    return jsonify({
        "public_key": SERVER_PUBLIC_KEY_BYTES.decode("utf-8"),
        "certificate": PK_CERT
    })


#Weather API to send the json data -- called by the client
@app.post("/weather")
def weather():
    body = request.get_json(silent=True)
    if not body or "encrypted_session_key" not in body:
        return jsonify({"error": "Missing encrypted_session_key"}), 400

    try:
        #Fetching session key created by the client (valid only for this api call)
        enc_session_key = base64.b64decode(body["encrypted_session_key"])

        # Decrypting AES session key with server private RSA key
        cipher_rsa = PKCS1_OAEP.new(SERVER_PRIVATE_KEY)
        session_key = cipher_rsa.decrypt(enc_session_key)

        plaintext = json.dumps(DATA).encode("utf-8")

        # Encrypting response with AES-GCM using the session key
        cipher_aes = AES.new(session_key, AES.MODE_GCM)
        ciphertext, tag = cipher_aes.encrypt_and_digest(plaintext)

        #sending the ciphetext, tag and nonce as response
        return jsonify({
            "nonce": base64.b64encode(cipher_aes.nonce).decode("utf-8"),
            "ciphertext": base64.b64encode(ciphertext).decode("utf-8"),
            "tag": base64.b64encode(tag).decode("utf-8")
        })

    except Exception as e:
        return jsonify({"error": f"Key exchange or encryption failed: {str(e)}"}), 400








#API for client to call and get the public key from server
# @app.get("/public-key")
# def get_public_key():
#     return jsonify({
#         "public_key": SERVER_PUBLIC_KEY.decode("utf-8")
#     })


# @app.post("/weather")
# def weather():
#     body = request.get_json(silent=True)
#     if not body or "encrypted_session_key" not in body: #checking the public key is in header
#         return jsonify({"error": "Missing encrypted_session_key"}), 400

#     try:
#         enc_session_key = base64.b64decode(body["encrypted_session_key"])

#         # Decrypting session key with RSA private key. This session key will be used for exchaning messages from now
#         cipher_rsa = PKCS1_OAEP.new(SERVER_PRIVATE_KEY)
#         session_key = cipher_rsa.decrypt(enc_session_key)

#         plaintext = json.dumps(DATA).encode("utf-8")

#         # Encrypting payload with fresh AES-GCM nonce
#         cipher_aes = AES.new(session_key, AES.MODE_GCM)
#         ciphertext, tag = cipher_aes.encrypt_and_digest(plaintext)

#         return jsonify({
#             "nonce": base64.b64encode(cipher_aes.nonce).decode("utf-8"),
#             "ciphertext": base64.b64encode(ciphertext).decode("utf-8"),
#             "tag": base64.b64encode(tag).decode("utf-8")
#         })

#     except Exception as e:
#         return jsonify({"error": f"Decryption/encryption failed: {str(e)}"}), 400


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5037, debug=False)