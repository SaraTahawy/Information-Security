# InfoSec Management Task2

## About the Project
This is a simple RESTful API using Flask to manage users and products.  
It uses `JWT` for authentication and protects some operations like adding and updating products.

##  Technologies Used
- **Flask** (for building the API)
- **Flask SQLAlchemy** (for database management)
- **Flask JWT Extended** (for authentication using `JWT`)
- **MySQL** (the database)
- **bcrypt** (for password hashing)
- **dotenv** (to store environment variables)

##  How to Run the Project
**Install required dependencies:**  
pip install flask flask_sqlalchemy flask_jwt_extended pymysql bcrypt python-dotenv

## Create a .env file (file to store database and authentication secrets) and add the following:
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=info_mgmt_sec_section5
JWT_SECRET_KEY=super_secret_key

## Run the application:
python task2.py

## Test the API using Postman:
POST /signup → Register a new user
POST /login → Authenticate and get a JWT token
PUT /users/{id} → Update user details (JWT required)
POST /products → Add a new product (JWT required)
GET /products → Retrieve all products
GET /products/{pid} → Retrieve a product by ID
PUT /products/{pid} → Update a product (JWT required)
DELETE /products/{pid} → Delete a product (JWT required)

## Author:
Sara Nabil Tahawy
