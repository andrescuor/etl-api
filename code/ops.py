from fastapi import UploadFile, HTTPException
from data_ops import process_csv, insert_batch

async def upload_csv(file: UploadFile):
    try:
        # Procesar el archivo CSV y cargarlo en la base de datos
        result = process_csv(file)
        return {"filename": file.filename, "status": "success", "rows_inserted": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def batch_insert(data: list):
    try:
        if not data:
            raise HTTPException(status_code=400, detail="No data provided")
        
        # Insertar el batch de datos en la base de datos
        result = insert_batch(data)
        return {"status": "success", "rows_inserted": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
