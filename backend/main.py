from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

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
    return {"filename": file.filename}

@app.get("/download/{filename}")
def download_file(filename: str, username: str, password: str):
    # Check authentication
    if username != USER or password != PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    file_path = f"uploads/{filename}"
    return FileResponse(path=file_path, filename=filename)

# Making sure uploads dir exists
import os
os.makedirs("uploads", exist_ok=True)
