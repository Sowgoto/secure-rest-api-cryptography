from pathlib import Path
import json
import base64

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15


#USED for creating certificates


STUDENT_ID = "11762337" #EUID of Sunny


def main():
    script_dir = Path(__file__).resolve().parent
    ca_dir = script_dir.parent / "keygen_ca"
    public_key_path = script_dir.parent / "keygen" #pointing to the keygen folder
    public_key_path = public_key_path / "public.key" #pointing to the keygen_ca folder
    secret_ca_key_path = ca_dir / "secret_ca.key"
    cert_path = script_dir / "pk.cert" #saving in the current folder

    public_key_bytes = public_key_path.read_bytes()
    public_key_hex = public_key_bytes.hex()

    #message that will be signed and saved
    message = (
        f"This public key: {public_key_hex} "
        f"belongs to {STUDENT_ID}."
    ).encode("utf-8")

    ca_private_key = RSA.import_key(secret_ca_key_path.read_bytes())

    h = SHA256.new(message)
    signature = pkcs1_15.new(ca_private_key).sign(h) #creating signature

    #message and it's signature --- signed by CA. It signs the public key of the server.
    cert_data = {
        "message": message.decode("utf-8"),
        "signature": base64.b64encode(signature).decode("utf-8")
    }

    #the signature is stored
    cert_path.write_text(json.dumps(cert_data, indent=2), encoding="utf-8")

    print("Public-key certificate created successfully.")
    print(f"Certificate saved to: {cert_path}")


if __name__ == "__main__":
    main()