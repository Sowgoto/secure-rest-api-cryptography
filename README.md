# Secure REST API with Cryptographic Protection

## Overview

This project demonstrates the step-by-step evolution of a basic REST API into a more secure communication system using cryptographic techniques.

The project begins with a simple plaintext REST client-server application and gradually improves its security by adding confidentiality, integrity, authenticated encryption, replay protection, public-key key exchange, and certificate-based public-key verification.

The project was implemented in Python using Flask, Requests, PyCryptodome, and Wireshark.

## Educational Use Only

This project is created for academic and educational purposes. It is intended to demonstrate secure communication concepts in a controlled local environment.

## Features

- Basic REST client-server communication
- Plaintext traffic analysis using Wireshark
- AES-CTR encryption for confidentiality
- HMAC for integrity and authentication
- AES-GCM authenticated encryption
- Replay attack demonstration
- Replay protection using a fresh client challenge
- RSA-based session key exchange
- Certificate authority simulation
- Server public-key verification
- Secure encrypted weather API communication

## Project Flow

The project follows these stages:

1. Basic REST client-server communication
2. Symmetric-key protection using AES-CTR and HMAC
3. Authenticated encryption using AES-GCM
4. Replay attack demonstration
5. Replay protection using a fresh client challenge
6. Public-key key exchange using RSA
7. Certificate-based public-key verification
8. Final secure REST communication

## Technologies Used

- Python
- Flask
- Requests
- PyCryptodome
- Wireshark
- RSA
- AES-CTR
- AES-GCM
- HMAC
- Digital certificates

## Repository Structure

```text
secure-rest-api/
│
├── README.md
├── client/
├── client_updated/
├── fake_server/
├── server/
├── server_updated/
├── super_fake_server/
├── keygen/
├── keygen_ca/
└── SECURE_REST_API_FINAL.pdf
```

## Requirements

Install the required Python libraries:

```bash
pip install flask requests pycryptodome
```

## How to Run

Start the basic server:

```bash
python server.py
```

Run the basic client:

```bash
python client.py
```

For the updated secure version, run the updated server and client files from their respective folders.

Example:

```bash
python server_updated.py
python client_updated.py
```

Commands may need to be adjusted depending on the folder structure and file names.

## Security Notes

Do not upload or share private key files such as:

```text
secret.key
secret_ca.key
private.key
*.pem
```

Public keys and generated certificates are for demonstration only. This project is not intended to replace production security mechanisms such as TLS/HTTPS.

## Demo Video

Project demonstration video:

https://www.youtube.com/watch?v=T8NzoA_v2go

## Project Report

The full project report is included in this repository as:

```text
SECURE_REST_API_FINAL.pdf
```

## Disclaimer

This project is for academic and educational purposes only. It demonstrates secure REST API communication and cryptographic design concepts in a local testing environment.

This project should not be used as a production-ready security implementation.

## Author

Sowgoto Raha Sunny  
M.S. in Cybersecurity  
University of North Texas

Arup Datta  
Sowgoto Raha Sunny  
M.S. in Cybersecurity  
University of North Texas
