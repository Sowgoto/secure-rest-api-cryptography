import requests
import json
import base64
from pathlib import Path

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15


# This is the student ID that we expect in the certificate message (We used Sunny's euid)
EXPECTED_STUDENT_ID = "11762337"


# CLIENT_DIR contains folder where this client file exists
# PROJECT_DIR contains parent folder of the client folder
# CA_DIR is the folder that contains CA-generated keys
CLIENT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = CLIENT_DIR.parent
CA_DIR = PROJECT_DIR / "keygen_ca"

# Path to the CA public key
PUBLIC_CA_KEY_PATH = CA_DIR / "public_ca.key"


# Loading the CA public key from the file
CA_PUBLIC_KEY = RSA.import_key(PUBLIC_CA_KEY_PATH.read_bytes())


def verify_server_certificate(server_public_key_pem: str, certificate: dict) -> bool:
    try:
        # Fetching the message and signature from the certificate
        message_str = certificate["message"]
        signature_b64 = certificate["signature"]

        # Convert the message into bytes
        message_bytes = message_str.encode("utf-8")
        signature = base64.b64decode(signature_b64)

        # Rebuild the exact message that should have been signed by the CA. Used for matching with signed message.
        server_public_key_bytes = server_public_key_pem.encode("utf-8")
        expected_message = (
            f"This public key: {server_public_key_bytes.hex()} "
            f"belongs to {EXPECTED_STUDENT_ID}."
        ).encode("utf-8")

        # First check if the received certificate message matches what we expect and if it does not match, then we should reject it
        if message_bytes != expected_message:
            return False

        # Verifying the CA signature on that message
        h = SHA256.new(message_bytes)
        pkcs1_15.new(CA_PUBLIC_KEY).verify(h, signature)
        return True

    except (ValueError, TypeError, KeyError):
        # Returning False if verification fails
        return False


def main():
    # Base URL of the server
    base_url = "http://127.0.0.1:5037"

    try:
        # Fetching the server's public key and certificate
        identity_resp = requests.get(f"{base_url}/server-identity", timeout=5)
        identity_resp.raise_for_status()

        # Parsing the server response as JSON
        identity = identity_resp.json()
        server_public_key_pem = identity["public_key"]
        certificate = identity["certificate"]

        # Verifying the server certificate
        if not verify_server_certificate(server_public_key_pem, certificate):
            print("Rejected: server certificate verification failed.")
            return

        print("Server certificate verified successfully.")

        # Importing the verified server public key
        server_public_key = RSA.import_key(server_public_key_pem)

        # Generating a random 32-byte AES session key
        session_key = get_random_bytes(32)  

        # Encrypting the session key using the server's RSA public key
        cipher_rsa = PKCS1_OAEP.new(server_public_key)
        enc_session_key = cipher_rsa.encrypt(session_key)

        # Sending the encrypted session key to the server
        weather_resp = requests.post(
            f"{base_url}/weather",
            json={
                "encrypted_session_key": base64.b64encode(enc_session_key).decode("utf-8")
            },
            timeout=5
        )
        weather_resp.raise_for_status()

        # Reading the encrypted response from the server
        encrypted_payload = weather_resp.json()

        # Decoding the nonce, ciphertext, and authentication tag from base64
        nonce = base64.b64decode(encrypted_payload["nonce"])
        ciphertext = base64.b64decode(encrypted_payload["ciphertext"])
        tag = base64.b64decode(encrypted_payload["tag"])

        # Creating AES-GCM cipher using the session key and nonce
        cipher_aes = AES.new(session_key, AES.MODE_GCM, nonce=nonce)

        # Decrypting the ciphertext and verify the authentication tag
        plaintext = cipher_aes.decrypt_and_verify(ciphertext, tag)

        # Converting the decrypted plaintext into JSON
        data = json.loads(plaintext.decode("utf-8"))

        print("Key exchange successful.")
        print("Decryption and authentication successful.\n")
        print("Decrypted JSON response:")
        for k, v in data.items():
            print(f"  {k}: {v}")

    except ValueError:
        print("Rejected: authentication failed.")
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
    except Exception as e:
        print("Unexpected error:", e)


if __name__ == "__main__":
    main()