from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from datetime import datetime

app = FastAPI()

# Configs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# User name and password
USER = "master"
PASSWORD = "123456"

def check_auth(username: str = Form(...), password: str = Form(...)):
    if username != USER or password != PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return username

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    if username == USER and password == PASSWORD:
        return {"success": True}
    else:
        raise HTTPException(status_code=401, detail="Bad credentials")

@app.post("/upload/")
def upload_file(file: UploadFile = File(...), username: str = Form(...), password: str = Form(...)):
    # Check authentication
    if username != USER or password != PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Save the file to uploads directory
    with open(f"uploads/{file.filename}", "wb") as buffer:
        buffer.write(file.file.read())
    
    # Add file to index
    add_file_to_index(file.filename, os.path.getsize(f"uploads/{file.filename}"), datetime.now().isoformat())
    
    return {"filename": file.filename}

@app.get("/download/{filename}")
def download_file(filename: str, username: str, password: str):
    # Check authentication
    if username != USER or password != PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    file_path = f"uploads/{filename}"
    return FileResponse(path=file_path, filename=filename)

# Index file management
INDEX_FILE = "uploads/file_index.json"

def load_file_index():
    """Load the file index from JSON file"""
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r") as f:
            return json.load(f)
    return {}

def save_file_index(index):
    """Save the file index to JSON file"""
    with open(INDEX_FILE, "w") as f:
        json.dump(index, f, indent=2)

def add_file_to_index(filename, file_size, upload_time):
    """Add a new file entry to the index"""
    index = load_file_index()
    index[filename] = {
        "filename": filename,
        "size": file_size,
        "upload_time": upload_time,
        "file_path": f"uploads/{filename}"
    }
    save_file_index(index)

# Making sure uploads dir exists
os.makedirs("uploads", exist_ok=True)
