# Usamos la imagen oficial de PostgreSQL
FROM postgres:15-alpine

# Configuración de las variables de entorno para PostgreSQL
ENV POSTGRES_USER=userglobant
ENV POSTGRES_PASSWORD=globantde2024
ENV POSTGRES_DB=company_db

# Copiar archivos de configuración adicionales (opcional)
COPY ./init.sql /docker-entrypoint-initdb.d/

# Exponer el puerto de PostgreSQL
EXPOSE 5432

# Comando de inicio predeterminado (no es necesario cambiarlo)
CMD ["postgres"]
