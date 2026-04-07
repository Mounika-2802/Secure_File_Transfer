from fastapi import FastAPI, UploadFile, File, Form
import os

app = FastAPI()
UPLOAD_DIR = "encrypted_vault"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_chunk(
    file_id: str = Form(...),
    chunk_index: int = Form(...),
    file: UploadFile = File(...)
):
    # Create a folder for each file_id
    file_path = os.path.join(UPLOAD_DIR, file_id)
    os.makedirs(file_path, exist_ok=True)
    
    # Save the encrypted chunk
    save_path = os.path.join(file_path, f"chunk_{chunk_index}.bin")
    with open(save_path, "wb") as f:
        f.write(await file.read())
        
    return {"status": "success", "chunk": chunk_index}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)