import os
import requests
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

CHUNK_SIZE = 64 * 1024  # 64KB
SERVER_URL = "http://127.0.0.1:8000/upload"

def secure_upload(file_path, key_path):
    # 1. Load Key
    with open(key_path, "rb") as f:
        key = f.read()
    aesgcm = AESGCM(key)
    
    file_id = os.urandom(8).hex()
    chunk_index = 0

    # 2. Read and Encrypt
    with open(file_path, "rb") as f:
        while True:
            data = f.read(CHUNK_SIZE)
            if not data: break
            
            nonce = os.urandom(12)
            # Encrypts + adds Integrity Tag (GCM)
            ciphertext = aesgcm.encrypt(nonce, data, None)
            
            # 3. Send to Server
            payload = nonce + ciphertext # Combined for storage
            files = {'file': (f"chunk_{chunk_index}", payload)}
            data = {'file_id': file_id, 'chunk_index': chunk_index}
            
            response = requests.post(SERVER_URL, files=files, data=data)
            print(f"Uploaded chunk {chunk_index}: {response.status_code}")
            chunk_index += 1

if __name__ == "__main__":
    # Generate key if it doesn't exist
    if not os.path.exists("master.key"):
        with open("master.key", "wb") as f:
            f.write(AESGCM.generate_key(bit_length=256))
            
    secure_upload("test.txt", "master.key")