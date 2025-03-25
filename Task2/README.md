استخدم التنسيق التالي ليظهر المحتوى منظمًا في ملف `README.md`:  

```markdown
# InfoSec Management Task2

## 📌 About the Project
This is a simple **RESTful API** using **Flask** to manage users and products.  
It uses `JWT` for authentication and protects operations like adding and updating products.

---

## 🛠️ Technologies Used
- 🚀 **Flask** → Backend framework  
- 🗄 **Flask SQLAlchemy** → Database management  
- 🔐 **Flask JWT Extended** → Authentication using `JWT`  
- 🛢 **MySQL** → Database  
- 🔑 **bcrypt** → Password hashing  
- 📝 **dotenv** → Store environment variables  

---

## 🚀 How to Run the Project
### 📌 Install Dependencies:
```bash
pip install flask flask_sqlalchemy flask_jwt_extended pymysql bcrypt python-dotenv
```

### 📌 Create a `.env` file and add:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=info_mgmt_sec_section5
JWT_SECRET_KEY=super_secret_key
```

### 📌 Run the Application:
```bash
python task2.py
```

---

## 🔥 API Endpoints (Test with Postman)
| Method | Endpoint | Description | Authentication |
|--------|---------|------------|---------------|
| **POST** | `/signup` | Register a new user | ❌ Not Required |
| **POST** | `/login` | Authenticate & get a JWT token | ❌ Not Required |
| **PUT** | `/users/{id}` | Update user details | ✅ `JWT Required` |
| **POST** | `/products` | Add a new product | ✅ `JWT Required` |
| **GET** | `/products` | Retrieve all products | ❌ Not Required |
| **GET** | `/products/{pid}` | Retrieve a product by ID | ❌ Not Required |
| **PUT** | `/products/{pid}` | Update a product | ✅ `JWT Required` |
| **DELETE** | `/products/{pid}` | Delete a product | ✅ `JWT Required` |

---

📌 **Note:** Use **Postman** or any API testing tool to test the endpoints.  
🛠 **Make sure the database is running** before executing requests.


