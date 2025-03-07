# Expenser

**Expenser** is a personal expense tracker web application built with Django and Bootstrap. It allows users to manage their expenses, view reports, and export their data in CSV, PDF, and Excel formats. It includes features like user authentication, CRUD operations for expenses, filtering, sorting, and more!

---

## Features

- **User Authentication**: 
  - Sign Up, Login, Logout, Update Password, and Delete User.
  - Edge Cases handled: After logging in, users cannot access the login or registration pages.
  - Dynamic navigation updates based on user login/logout status.

- **Expense Management**:
  - Create, Edit, and Delete expenses.
  - Categorize expenses using predefined or user-defined categories.
  - Description is optional.
  - List expenses and the ability to view each expense in detail.

- **Filtering, Sorting, and Searching**:
  - Filter expenses by amount, date range, and categories.
  - Sort expenses by title, amount, category, and date.
  - Search expenses by title or category.

- **Export Options**:
  - Export expenses to CSV, PDF, or Excel files for better reporting.

- **Charts**:
  - Visualize your expenses using charts to help understand spending patterns.

- **Mobile-Friendly**:
  - Fully responsive design for use on various devices.

---

## Tech Stack

- **Backend**: Django
- **Frontend**: HTML, CSS, Bootstrap 5
- **Database**: MySQL (or any other SQL database of your choice)
- **Charting**: Chart.js
- **File Export**: Pandas, ReportLab for PDFs
- **Authentication**: Django's built-in user authentication system

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/gurdeepkumar/expenser.git
cd expenser
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a .env file in the project root with the following:
```bash
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
DEBUG=True
ALLOWED_HOSTS=your_allowed_hosts
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create a superuser for admin access

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```
The app will be running at http://127.0.0.1:8000/.

# **API Documentation**

## **Authentication**

To access the API, you need to authenticate using a Bearer token. You can obtain this token by creating an account with **Expenser** and navigating to the **API section** of your account.

Once you have registered and logged in, you can generate your token in the API section.

### **Example of Authentication (Bearer Token)**

> Authorization: Token YOUR_ACCESS_TOKEN

## **Error Codes**

- **400 Bad Request**: Invalid request format or data.
- **401 Unauthorized**: Authentication failed or token expired.
- **404 Not Found**: The requested resource was not found.
- **500 Internal Server Error**: A server error occurred.

## **Endpoints**

### **1. Get All Expenses**

- **URL**: `/expenses/api/expenses/`
- **Method**: `GET`
- **Description**: Retrieve all expenses for the authenticated user.

---

### **2. Create Expense**

- **URL**: `/expenses/api/expenses/create/`
- **Method**: `POST`
- **Description**: Create a new expense.

---

### **3. Get Expense Detail**

- **URL**: `/expenses/api/expenses/<int:pk>/`
- **Method**: `GET`
- **Description**: Retrieve the details of a specific expense by its ID.
---

### **4. Update Expense**

- **URL**: `/expenses/api/expenses/<int:pk>/update/`
- **Method**: `PUT`
- **Description**: Update an existing expense by its ID.
---

### **5. Delete Expense**

- **URL**: `api/expenses/<int:pk>/delete/`
- **Method**: `DELETE`
- **Description**: Delete an expense by its ID.
---


## License

This project is licensed under the MIT License - see the LICENSE file for details.
