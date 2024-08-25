import pandas as pd
from sqlalchemy import create_engine
from io import StringIO
from fastapi import UploadFile

# Configuración de la base de datos
DATABASE_URL = "postgresql+psycopg2://user:password@localhost/dbname"
engine = create_engine(DATABASE_URL)

def process_csv(file: UploadFile):
    # Leer el archivo CSV en un DataFrame de pandas
    content = file.file.read().decode('utf-8')
    df = pd.read_csv(StringIO(content))
    
    # Validar y limpiar el DataFrame si es necesario (aquí puedes agregar más lógica)
    cleaned_df = validate_and_clean_data(df)
    
    # Definir el nombre de la tabla basada en el nombre del archivo
    table_name = file.filename.split('.')[0]
    
    # Guardar el DataFrame en la base de datos
    cleaned_df.to_sql(
        name=table_name,
        con=engine,
        if_exists='append',  # Puedes usar 'replace' si deseas sobrescribir los datos
        index=False
    )

    return len(cleaned_df)

def insert_batch(data: list):
    # Convertir los datos en un DataFrame de pandas
    df = pd.DataFrame(data)

    # Validar y limpiar el DataFrame si es necesario (aquí puedes agregar más lógica)
    cleaned_df = validate_and_clean_data(df)

    # Definir el nombre de la tabla basada en la primera entrada del dato
    table_name = data[0].get('table_name')
    
    if not table_name:
        raise ValueError("Table name not provided")

    # Guardar el DataFrame en la base de datos
    cleaned_df.to_sql(
        name=table_name,
        con=engine,
        if_exists='append',  # Puedes usar 'replace' si deseas sobrescribir los datos
        index=False
    )

    return len(cleaned_df)

def validate_and_clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # Aquí puedes implementar cualquier lógica de validación y limpieza necesaria
    # Por ejemplo, eliminar filas con valores nulos:
    df = df.dropna()
    
    # Aquí podrías agregar más transformaciones
    return df
