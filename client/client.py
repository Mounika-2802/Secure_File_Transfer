import os
import requests
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

CHUNK_SIZE = 64 * 1024 
URL = "http://127.0.0.1:8000"

def get_key():
    return open("master.key", "rb").read()

def secure_upload(file_path, file_id=None):
    aesgcm = AESGCM(get_key())
    if not file_id:
        file_id = os.urandom(4).hex()
    
    # RESUME SUPPORT: Ask server how many chunks it has
    res = requests.get(f"{URL}/status/{file_id}")
    start_chunk = res.json().get("chunks_found", 0)
    
    print(f"Starting upload for {file_id} from chunk {start_chunk}...")

    with open(file_path, "rb") as f:
        f.seek(start_chunk * CHUNK_SIZE) # Skip already uploaded data
        idx = start_chunk
        while chunk := f.read(CHUNK_SIZE):
            nonce = os.urandom(12)
            ciphertext = aesgcm.encrypt(nonce, chunk, None)
            
            requests.post(f"{URL}/upload", 
                          data={'file_id': file_id, 'chunk_index': idx}, 
                          files={'file': nonce + ciphertext})
            print(f"Uploaded chunk {idx}")
            idx += 1
    return file_id

def secure_download(file_id, output_name, total_chunks):
    aesgcm = AESGCM(get_key())
    with open(output_name, "wb") as out_f:
        for idx in range(total_chunks):
            r = requests.get(f"{URL}/download/{file_id}/{idx}")
            raw = r.content
            nonce, ciphertext = raw[:12], raw[12:]
            
            # Integrity Check (HMAC equivalent)
            decrypted = aesgcm.decrypt(nonce, ciphertext, None)
            out_f.write(decrypted)
            print(f"Decrypted chunk {idx}")
