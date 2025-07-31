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
def upload_file(file: UploadFile = File(...), user: str = Depends(check_auth)):
    # Save the file to backend/uploads
    with open(f"backend/uploads/{file.filename}", "wb") as buffer:
        buffer.write(file.file.read())
    return {"filename": file.filename}

@app.get("/download/{filename}")
def download_file(filename: str, user: str = Depends(check_auth)):
    file_path = f"backend/uploads/{filename}"
    return FileResponse(path=file_path, filename=filename)

# Making sure uploads dir exists
import os
os.makedirs("backend/uploads", exist_ok=True)
