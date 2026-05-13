from Crypto.PublicKey import RSA
from pathlib import Path

#used the same code as keygen.py

def main():
   
    key = RSA.generate(2048) #creating public and private key pairs

    #Exporing public and private key
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    script_dir = Path(__file__).resolve().parent #trying to save the keys in the same folder as the code

    # Saving private key in the current folder
    with open(script_dir / "secret_ca.key", "wb") as f:
        f.write(private_key)

     # Saving private key in the current folder
    with open(script_dir / "public_ca.key", "wb") as f:
        f.write(public_key)

    print("RSA key pair generated successfully.")
    print("Public key saved to public_ca.key")
    print("Private key saved to secret_ca.key")


if __name__ == "__main__":
    main()