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
