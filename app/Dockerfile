FROM python:3.10-slim

# Create  Docker Work dir
WORKDIR /app


# Install Dependencies

COPY ./app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y \
    libpq-dev  # Necesario para psycopg2

# PORT TO EXPOSE
EXPOSE 8000

# COPY CODE
COPY ./app /app



# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]