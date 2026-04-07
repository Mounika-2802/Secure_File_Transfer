# Encrypted File Transfer & Secure Storage

A practical implementation of a Zero-Knowledge file transfer system using AES-256-GCM.

## 🛡️ Features
- **AES-256-GCM:** Authenticated encryption that ensures both privacy and data integrity.
- **Client-Side Encryption:** The server never sees the raw data or the encryption key.
- **File Chunking:** Large files are broken into 64KB chunks to optimize memory.
- **Secure Storage:** Files are stored as encrypted binary blobs on the server disk.

## 🕵️ Threat Model & Mitigation
| Threat | Mitigation |
| :--- | :--- |
| **Man-in-the-Middle** | Payloads are encrypted; TLS/HTTPS should be used for transport. |
| **Server Tampering** | AES-GCM Authentication Tags: Decryption fails if a single bit is changed. |
| **Storage Breach** | Data is "at-rest" encrypted. Stolen files are useless without the `master.key`. |
| **Key Management** | Keys are stored locally on the client and never shared with the server. |

## 🚀 How to Run
1. Install requirements: `pip install fastapi uvicorn cryptography requests`
2. Start server: `cd server && python main.py`
3. Run client: `cd client && python client.py`

