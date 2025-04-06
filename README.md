# 📝 Text-to-SQL Project

This project converts natural language questions into SQL queries using Google's Gemini API, executes them on a MySQL database, and returns the result. It includes:

- 🖥️ **Django Backend** (Text-to-SQL API)
- 🌐 **Angular Frontend** (User Interface to ask questions)

---

## 🧠 Tech Stack

- **Backend:** Django, Django REST Framework, Google Gemini API, MySQL  
- **Frontend:** Angular  
- **Database:** MySQL  

---

## ⚙️ Backend Setup (Django)

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd <backend-folder>
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

```bash
pip install django djangorestframework python-dotenv mysql-connector-python google-generativeai
```

### 4. Configure environment variables
Create a .env file in the root directory:

```ini
GOOGLE_API_KEY=your_google_api_key
```

### 5. Set up MySQL database
Ensure MySQL server is running and create a database named institute with the following tables:

```sql
CREATE TABLE student (
  SID INT PRIMARY KEY,
  FName VARCHAR(50),
  LName VARCHAR(50),
  Phone VARCHAR(15),
  GPA FLOAT,
  Department VARCHAR(50),
  Joining_Year INT,
  Passing_Year INT
);

CREATE TABLE instructor (
  IID INT PRIMARY KEY,
  FName VARCHAR(50),
  LName VARCHAR(50),
  Department VARCHAR(50)
);

CREATE TABLE courses (
  CID INT PRIMARY KEY,
  Title VARCHAR(100),
  Credits INT
);

CREATE TABLE takes (
  SID INT,
  CID INT,
  Semester VARCHAR(10)
);

CREATE TABLE teaches (
  IID INT,
  CID INT,
  Semester VARCHAR(10)
);
```

Note:
Update MySQL credentials in Django code inside the get_sql_response function.

### 6. Run the Django server
```bash
python manage.py runserver
```
API available at: http://127.0.0.1:8000/

## 🖼️ Frontend Setup (Angular)
### 1. Navigate to frontend folder
```bash
cd <angular-project-folder>
```

### 2. Install Angular CLI (if not already installed)
```bash
npm install -g @angular/cli
```

### 3. Install dependencies
```bash
npm install
```

### 4. Serve the Angular app
```bash
ng serve
```
App runs by default at: http://localhost:4200

✅ Ensure the Angular app makes POST requests to Django backend at http://127.0.0.1:8000/

## 🔄 CORS Configuration (Optional but Recommended)
Install Django CORS headers:

```bash
pip install django-cors-headers
```

In settings.py:

```python
INSTALLED_APPS = [
    ...
    'corsheaders',
    ...
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]

CORS_ALLOW_ALL_ORIGINS = True  # For development only
```

## 🚀 Project Structure Overview
```bash
├── backend/
│   ├── .env
│   ├── views.py      # main logic
│   ├── manage.py
│   └── ...
└── frontend/
    ├── src/
    ├── angular.json
    └── ...
```