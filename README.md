# 📚 Library Management System

## 🚀 Project Overview

This project is a **Library Management System** developed using **Python (Flask) and MySQL**.
It helps manage books, memberships, transactions, and reports in a library.

The system supports both **Admin** and **User** roles with different functionalities.

---

## 🛠️ Technologies Used

* Python (Flask)
* MySQL Database
* HTML, CSS
* Jinja2 Templates

---

## 👤 User Roles

### 🔹 Admin

* Manage books and memberships
* View reports
* Handle transactions

### 🔹 User

* Check book availability
* Issue and return books
* View reports

---

## 📌 Features

### 🔐 Login System

* Admin Login
* User Login

---

### 🏠 Home Pages

* Admin Home Page
* User Home Page

---

### 🔄 Transactions

* Check Book Availability
* Search Books
* Issue Book
* Return Book
* Pay Fine

---

### 📊 Reports

* Master List of Books
* Master List of Memberships
* Active Issues
* Overdue Returns
* Issue Requests

---

### 🛠️ Maintenance (Admin Only)

* Add Book
* Update Book
* Add Membership
* Update Membership
* User Management

---

### 📄 Other Pages

* Confirmation Page
* Cancel Page
* Logout Page

---

## 🗄️ Database Structure

### Tables Used:

* users
* books
* memberships
* issues

---

## ⚙️ Installation & Setup

### Step 1: Install Dependencies

```bash
pip install flask mysql-connector-python
```

---

### Step 2: Setup Database

* Open MySQL Workbench
* Run `schema.sql` file

---

### Step 3: Configure Database

Update `db.py` file:

```python
password="your_mysql_password"
```

---

### Step 4: Run the Project

```bash
python app.py
```

---

### Step 5: Open in Browser

```
http://127.0.0.1:5000
```

---

## 🔑 Default Login Credentials

### Admin

* Username: adm
* Password: adm

### User

* Username: user
* Password: user



