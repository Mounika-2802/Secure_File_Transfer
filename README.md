# 🛡️ SecureCloud: Encrypted File Transfer & Storage

A high-security file transfer system implementing **Zero-Knowledge Architecture**. Files are encrypted on the client side using **AES-256-GCM** before reaching the server.

## 🛠️ Implementation Details
- **AES-256-GCM (AEAD):** Provides Confidentiality and Authenticity. If a single bit is changed on the server, decryption fails.
- **Chunked Transfer:** Supports large files by splitting them into 64KB segments.
- **Resume Support:** Checks server status before uploading to skip existing chunks.
- **Zero-Knowledge:** The server stores `.bin` blobs but never receives the `master.key`.

## 🕵️ Threat Model
| Threat | Mitigation |
| :--- | :--- |
| **Man-in-the-Middle** | Payloads are pre-encrypted. *Note: In production, TLS/HTTPS is required to protect metadata.* |
| **Server-Side Breach** | Even if the database is stolen, files remain encrypted blobs without the client-side key. |
| **Data Corruption** | Built-in integrity tags (GCM) detect any unauthorized modifications on disk. |

## 🚀 Usage
1. **Server:** `cd server && python main.py`
2. **Client Upload:** Call `secure_upload("file.zip")`
3. **Client Download:** Call `secure_download("file_id", "restored.zip", total_chunks)`

🛠️ **Practical Implementation Workflow**

This project follows a Zero-Knowledge security model. Here is the step-by-step process of how a file is handled:

**_1. Client-Side Preparation_**

Key Generation: A 256-bit AES key is generated locally (master.key). This key never leaves the client's machine.

File Chunking: The source file is read in 64KB chunks. This allows the system to handle GB-sized files without crashing the RAM and supports Resume Uploads.

**_2. The Encryption Process (AES-256-GCM)_**

For every chunk, the client:

Generates a unique 12-byte Nonce (Initialization Vector).

Encrypts the data using AES-GCM.

Produces a 16-byte Authentication Tag (Integrity Check).

Prepends the Nonce to the Ciphertext for storage.

**_3. Secure Transfer & Storage_**

Handshake: The client checks the server for existing chunks (/status/{file_id}) to skip already uploaded data.

Upload: Chunks are sent via POST requests.

Server Role: The server receives the encrypted binary blob and saves it to the encrypted_vault/. The server cannot read the file because it lacks the master.key.

**_4. Retrieval & Integrity Verification_**

Download: Chunks are fetched individually from the server.

Authentication: During decryption, the GCM Tag is verified. If the server (or a hacker) modified even 1 bit of the encrypted file, the cryptography library will throw an InvalidTag error, and the process will stop.

Reassembly: Validated chunks are written sequentially to reconstruct the original file.
