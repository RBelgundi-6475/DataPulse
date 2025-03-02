-- Database creation
CREATE DATABASE Test_DB;
GO
USE Test_DB;

-- Table creation
CREATE TABLE employee (id INTEGER IDENTITY(1001,1) NOT NULL PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,  
            email VARCHAR(255) NOT NULL UNIQUE,
			salary INTEGER);
INSERT INTO employee(first_name,last_name,email,salary)
  VALUES ('Jeff','Thomas','thomas.jeff@afer.com',10000),
  ('Sasha','Bailey','s.bailey@foobar.com',20000),
  ('Edward','Hart','edhart@walker.com',NULL);

-- Enable CDC at DB level
USE Test_DB;
EXEC sys.sp_cdc_enable_db;
ALTER DATABASE Test_DB SET CHANGE_TRACKING = ON (CHANGE_RETENTION = 2 DAYS, 
                         AUTO_CLEANUP = ON);

			
-- Enable CDC at Table level
EXEC sys.sp_cdc_enable_table @source_schema = 'dbo', @source_name = 'employee', @role_name = NULL,
@capture_instance='employee_instance', @supports_net_changes = 1;

-- source_schema is the database object
-- source_name is the table name
-- capture_instance is the name of the instance of the CDC enabled table

UPDATE employee
SET salary = 900  -- Set your desired salary here
WHERE email = 'edhart@walker.com';

INSERT INTO employee (first_name, last_name, email, salary) VALUES
('Alice', 'Johnson', 'alice.johnson@example.com', 75000),
('Bob', 'Smith', 'bob.smith@example.com', 68000),
('Charlie', 'Davis', 'charlie.davis@example.com', 72000),
('David', 'Williams', 'david.williams@example.com', 80000),
('Emma', 'Brown', 'emma.brown@example.com', 77000);


UPDATE employee
SET salary = 43000  -- Set your desired salary here
WHERE email = 'emma.brown@example.com';

UPDATE employee
SET salary = 1000  -- Set your desired salary here
WHERE email = 'thomas.jeff@afer.com';

UPDATE employee
SET salary = 100
WHERE email = 'thomas.jeff@afer.com';