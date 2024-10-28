from fastapi import FastAPI, UploadFile, File, HTTPException
from datetime import datetime
import os
import pandas as pd
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, DateTime
import asyncio
from typing import Dict, List
from collections import deque


UPLOAD_DIR = "/app/csvFiles/"
app = FastAPI()
processing_queue = deque()
column_mappings: Dict[str, List[str]] = {
    "departments": ["id", "department_name"],
    "hired_employees": ["id", "name", "hire_date", "department_id", "job_id"],
    "jobs": ["id", "job_title"]
}

pk_list = ["id"]
fk_list = ["department_id", "job_id"]

# Semáforo para controlar el acceso concurrente
processing_semaphore = asyncio.Semaphore(1)


@app.get("/")
async def initial_validation():

    return "API Funcionando ..."

@app.post("/upload-file/")
async def upload_file(file: UploadFile = File(...)):

    try:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename_with_timestamp = f"{timestamp}_{file.filename}"
        file_location = os.path.join(UPLOAD_DIR, filename_with_timestamp)

        #file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as f:
            f.write(file.file.read())
        

        # Extraer el nombre de la tabla del nombre del archivo
        table_name = os.path.splitext(file.filename)[0].lower()

        # Verificar si existe el mapping de columnas para esta tabla
        if table_name not in column_mappings:
            raise ValueError(f"The table {table_name} does not exist in the DDBB")

        # Agregar a la cola de procesamiento
        processing_queue.append({
            "file_location": file_location,
            "table_name": table_name,
            "original_filename": file.filename
        })
        
        # Procesar la cola
        await process_queue()

        return {
            "info": f"El archivo '{file.filename}' se agregó a la cola de procesamiento",
            "timestamp": timestamp,
            "position_in_queue": len(processing_queue)
        }
            
    
    except Exception as e:
        print("Data extract error: " + str(e))     
        #return {"info": f"file '{file.filename}' saved at '{file_location}'"}
        return HTTPException(status_code=500, detail=str(e))

async def process_queue():
    async with processing_semaphore:
        while processing_queue:
            try:
                file_info = processing_queue.popleft()
                file_location = file_info["file_location"]
                table_name = file_info["table_name"]

                # Leer CSV con las columnas correspondientes
                df = pd.read_csv(
                    file_location, 
                    header=None, 
                    names=column_mappings[table_name]
                )
                
                df, cleaning_report = clean_data(df, table_name)
                # Cargar datos
                await load(df, table_name)

                print(f"Archivo {file_info['original_filename']} procesado exitosamente")

            except Exception as e:
                print(f"Error procesando archivo: {str(e)}")
                # Volver a agregar a la cola en caso de error
                processing_queue.append(file_info)
                raise HTTPException(status_code=500, detail=str(e))

async def load(df, table_name):
    try:
        engine = create_engine('postgresql://admin:admin@postgres_ddbb:5432/company_db')
        metadata = MetaData()

        # Crear definición de tabla dinámica basada en el mapping
        columns = [Column('processed_at', DateTime)]
        for col_name in column_mappings[table_name]:
            if 'id' in col_name.lower():
                columns.append(Column(col_name, Integer))
            else:
                columns.append(Column(col_name, String))

        table = Table(table_name, metadata, *columns)
        metadata.create_all(engine)

        
        # Cargar datos
        df.to_sql(table_name, engine, if_exists='append', index=False)
        print(f"Datos importados exitosamente en la tabla '{table_name}'")

    except Exception as e:
        print("Error al cargar los datos en la base de datos: " + str(e))
        raise Exception(f"Error en la carga de datos: {str(e)}")

def clean_data(df: pd.DataFrame, table_name: str) -> tuple[pd.DataFrame, dict]:
    
    # Guardar el número original de filas
    original_rows = len(df)
    
    # Encontrar filas con valores nulos
    rows_with_nulls = df[df.isnull().any(axis=1)]
    
    # Eliminar filas con valores nulos
    df_clean = df.dropna()

    # Eliminar registros duplicados
    df_clean_no_duplicates = df_clean.drop_duplicates()
    
    # Contar el número de filas después de eliminar duplicados
    rows_after_cleaning = len(df_clean_no_duplicates)
    rows_removed_duplicates = len(df_clean) - rows_after_cleaning

    # Generar reporte solo si se eliminaron filas
    report = {
        "tabla": table_name,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "filas_originales": original_rows,
        "filas_eliminadas": len(rows_with_nulls) + rows_removed_duplicates,
        "filas_restantes": rows_after_cleaning,
        "detalle_filas_eliminadas": {
            "nulos": rows_with_nulls.to_dict('records'),
            "duplicados": df_clean[df_clean.duplicated()].to_dict('records')
        }
    } if len(rows_with_nulls) > 0 or rows_removed_duplicates > 0 else None
        
    return df_clean, report


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


