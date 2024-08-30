

-- Crear BBDD especial

CREATE DATABASE company_db;

-- Creación de la tabla Jobs
CREATE TABLE company_db.Jobs (
    Id SERIAL PRIMARY KEY, -- Identificador único para cada Job
    Job_Title VARCHAR(100) NOT NULL -- Título del trabajo, con un máximo de 100 caracteres
);

-- Creación de la tabla Departments
CREATE TABLE company_db.Departments (
    Id SERIAL PRIMARY KEY, -- Identificador único para cada Departamento
    Department_Name VARCHAR(100) NOT NULL -- Nombre del departamento, con un máximo de 100 caracteres
);

-- Creación de la tabla Hired_Employees
CREATE TABLE company_db.Hired_Employees (
    Id SERIAL PRIMARY KEY, -- Identificador único para cada empleado contratado
    Name VARCHAR(100) NOT NULL, -- Nombre del empleado
    Hire_Date TIMESTAMP NOT NULL, -- Fecha y hora de contratación
    Department_Id INT REFERENCES Departments(Id), -- Llave foránea que referencia a Departments
    Job_Id INT REFERENCES Jobs(Id), -- Llave foránea que referencia a Jobs
);
