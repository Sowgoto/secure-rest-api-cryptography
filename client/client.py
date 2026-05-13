import requests
import base64
import json
from Crypto.Cipher import AES

import hmac
import hashlib


#The client.py contains the code that is used to call the server


# This is the shared secret key used by both client and server
SECRET_KEY = b"super_secret_32_byte_key_for_aes"


# ---------------- STEP 2 ----------------
# In this step, the client receives encrypted data from the server and then decrypts it using AES in CTR mode.

# def main():
#     url = "http://127.0.0.1:5037/weather"  
#     try:
#         # Sending GET request to the server
#         resp = requests.get(url, timeout=5)
#         resp.raise_for_status()
#
#         # Getting the encrypted JSON response from the server
#         encrypted_payload = resp.json()
#
#         # Decoding the nonce and ciphertext from base64
#         nonce = base64.b64decode(encrypted_payload["nonce"])
#         ciphertext = base64.b64decode(encrypted_payload["ciphertext"])
#
#         # Creating AES cipher in CTR mode using the shared key and nonce
#         cipher = AES.new(SECRET_KEY, AES.MODE_CTR, nonce=nonce)
#
#         # Decrypting the ciphertext
#         decrypted_bytes = cipher.decrypt(ciphertext)
#
#         # Converting decrypted bytes into JSON format
#         data = json.loads(decrypted_bytes.decode('utf-8'))
#
#         print("Decrypted JSON response:")
#         for k, v in data.items():
#             print(f"  {k}: {v}")
#
#     except requests.exceptions.RequestException as e:
#         print("Request failed:", e)
#     except json.JSONDecodeError:
#         print("Data is corrupted! Decryption finished, but the result wasn't valid JSON.")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")


# ---------------- STEP 3 ----------------
# In this step, the communication is not encrypted. Instead, we are only checking integrity using HMAC.
# def main():
#     url = "http://127.0.0.1:5038/weather"
#     try:
#         # Sending request to the server
#         resp = requests.get(url, timeout=5)
#         resp.raise_for_status()
#
#         # Reading JSON response from the server
#         response_data = resp.json()
#         received_payload_str = response_data["payload"]
#         received_mac = response_data["mac"]
#
#         # Converting payload into bytes because HMAC works on bytes
#         payload_bytes = received_payload_str.encode('utf-8')
#
#         # Creating our own MAC from the received payload using the shared key
#         expected_mac = hmac.new(SECRET_KEY, payload_bytes, hashlib.sha256).hexdigest()
#
#         # Comparing our MAC with the server's MAC securely
#         if hmac.compare_digest(expected_mac, received_mac):
#             print("Authentication Successful!")
#             print("The data is authentic and has not been tampered with.\n")
#
#             # If MAC is correct, then load the actual JSON payload
#             data = json.loads(received_payload_str)
#             print("Status:", resp.status_code)
#             print("JSON response:")
#             for k, v in data.items():
#                 print(f"  {k}: {v}")
#
#             # Saving the MAC tag into a file for later use
#             with open("tag.txt", "w") as f:
#                 f.write(received_mac)
#             print("MAC tag successfully saved to 'tag.txt'")
#
#         else:
#             print("Authentication Failed!")
#     except requests.exceptions.RequestException as e:
#         print("Request failed:", e)


# ---------------- STEP 4 ----------------
# In this step, we use AES-GCM. AES-GCM gives both confidentiality and authentication.


def main():
    # This URL points to the real server
    url = "http://127.0.0.1:5037/weather"

    try:
        # Sending request to the server
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()

        # Saving the raw server response into a binary file
        with open("response.bin", "wb") as f:
            f.write(resp.content)

        # Reading the JSON object sent by the server
        encrypted_payload = resp.json()

        # Decoding the nonce, ciphertext, and tag from base64 format
        nonce = base64.b64decode(encrypted_payload["nonce"])
        ciphertext = base64.b64decode(encrypted_payload["ciphertext"])
        tag = base64.b64decode(encrypted_payload["tag"])

        # Creating AES cipher in GCM mode using the shared secret key and nonce
        cipher = AES.new(SECRET_KEY, AES.MODE_GCM, nonce=nonce)

        # Decrypting the ciphertext and also verifying the authentication tag
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)

        # Turning decrypted plaintext back into JSON data
        data = json.loads(plaintext.decode("utf-8"))

        print("Decryption and authentication successful!")
        print("Server response saved to 'response.bin'\n")
        print("Status:", resp.status_code)
        print("Decrypted JSON response:")
        for k, v in data.items():
            print(f"  {k}: {v}")

    except ValueError:
        print("Authentication failed! The ciphertext/tag is invalid or the data was tampered with.")
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
    except json.JSONDecodeError:
        print("Decryption succeeded, but the plaintext was not valid JSON.")
    except Exception as e:
        print("An unexpected error occurred:", e)


if __name__ == "__main__":
    main()