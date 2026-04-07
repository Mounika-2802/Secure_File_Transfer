from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
import os
import glob

app = FastAPI()
UPLOAD_DIR = "encrypted_vault"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_chunk(
    file_id: str = Form(...),
    chunk_index: int = Form(...),
    file: UploadFile = File(...)
):
    folder_path = os.path.join(UPLOAD_DIR, file_id)
    os.makedirs(folder_path, exist_ok=True)
    
    save_path = os.path.join(folder_path, f"chunk_{chunk_index}.bin")
    # Resume Support: If chunk exists, skip saving
    if os.path.exists(save_path):
        return {"status": "exists", "chunk": chunk_index}

    with open(save_path, "wb") as f:
        content = await file.read()
        f.write(content)
    return {"status": "success", "chunk": chunk_index}

@app.get("/status/{file_id}")
async def get_status(file_id: str):
    # Returns how many chunks we already have (for Resume Support)
    folder_path = os.path.join(UPLOAD_DIR, file_id)
    if not os.path.exists(folder_path):
        return {"chunks_found": 0}
    chunks = glob.glob(os.path.join(folder_path, "*.bin"))
    return {"chunks_found": len(chunks)}

@app.get("/download/{file_id}/{chunk_index}")
async def download_chunk(file_id: str, chunk_index: int):
    file_path = os.path.join(UPLOAD_DIR, file_id, f"chunk_{chunk_index}.bin")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Chunk not found")
