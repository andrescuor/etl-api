from fastapi import FastAPI, UploadFile, File, HTTPException
from ops import upload_csv, batch_insert
import os
import pandas as pd

UPLOAD_DIR = "/app/csvFiles/"
app = FastAPI()


@app.get("/")
async def initial_validation():

    return "API Funcionando ..."


@app.post("/upload-file/")
async def upload_file(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        f.write(file.file.read())
    return {"info": f"file '{file.filename}' saved at '{file_location}'"}


@app.get("/get-csv-fields/")
async def get_csv_fields(filename: str):
    # Verifica si el archivo existe en el directorio de subida
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    # Lee el archivo CSV en un DataFrame de pandas
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading CSV file: {str(e)}")
    
    # Convierte el DataFrame a JSON
    data = df.to_dict(orient="records")
    
    return {"filename": filename, "data": data}


@app.get("/validate-data/")
async def validate_data(table_name: str):
    if not engine.dialect.has_table(engine, table_name):
        return {"error": f"Table '{table_name}' does not exist"}
    
    query = f"SELECT * FROM {table_name} LIMIT 10"
    with engine.connect() as conn:
        result = conn.execute(query)
        rows = [dict(row) for row in result]
    
    return {"data": rows}


@app.post("/batch-insert/")
async def batch(data: list):
    return await batch_insert(data)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


