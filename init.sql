
-- Creación de la tabla Jobs
CREATE TABLE Jobs (
    Id SERIAL PRIMARY KEY,
    Job_Title VARCHAR(100) NOT NULL
);

-- Creación de la tabla Departments
CREATE TABLE Departments (
    Id SERIAL PRIMARY KEY,
    Department_Name VARCHAR(100) NOT NULL
);

-- Creación de la tabla Hired_Employees
CREATE TABLE Hired_Employees (
    Id SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Hire_Date TIMESTAMP NOT NULL,
    Department_Id INT REFERENCES Departments(Id),
    Job_Id INT REFERENCES Jobs(Id)
);
