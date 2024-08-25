from fastapi import FastAPI, UploadFile, File, HTTPException
from ops import upload_csv, batch_insert

app = FastAPI()

@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    return await upload_csv(file)

@app.get("/info-get/")
async def get_info():
    return {"message": "Welcome to the API!"}

@app.post("/batch-insert/")
async def batch(data: list):
    return await batch_insert(data)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


