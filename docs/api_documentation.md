# **Expenser API Documentation**

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
- **Response**:
    - **Status**: `200 OK`
    - **Body**:
      ```json
      [
        {
          "id": 1,
          "title": "Lunch",
          "amount": 15.5,
          "category": "Food",
          "description": "Lunch at cafe",
          "date": "2025-03-06T12:30:00Z"
        },
        {
          "id": 2,
          "title": "Transport",
          "amount": 30.0,
          "category": "Transport",
          "description": "Bus fare",
          "date": "2025-03-07T08:00:00Z"
        }
      ]
      ```

---

### **2. Create Expense**

- **URL**: `/expenses/api/expenses/create/`
- **Method**: `POST`
- **Description**: Create a new expense.
- **Body (JSON)**:
    ```json
    {
      "title": "Lunch",
      "amount": 15.5,
      "category": "Food",
      "description": "Lunch at cafe"
    }
    ```
- **Response**:
    - **Status**: `201 Created`
    - **Body**:
      ```json
      {
        "id": 3,
        "title": "Lunch",
        "amount": 15.5,
        "category": "Food",
        "description": "Lunch at cafe",
        "date": "2025-03-07T12:30:00Z"
      }
      ```

---

### **3. Get Expense Detail**

- **URL**: `/expenses/api/expenses/<int:pk>/`
- **Method**: `GET`
- **Description**: Retrieve the details of a specific expense by its ID.
- **Response**:
    - **Status**: `200 OK`
    - **Body**:
      ```json
      {
        "id": 1,
        "title": "Lunch",
        "amount": 15.5,
        "category": "Food",
        "description": "Lunch at cafe",
        "date": "2025-03-06T12:30:00Z"
      }
      ```

---

### **4. Update Expense**

- **URL**: `/expenses/api/expenses/<int:pk>/update/`
- **Method**: `PUT`
- **Description**: Update an existing expense by its ID.
- **Body (JSON)**:
    ```json
    {
      "title": "Dinner",
      "amount": 20.0,
      "category": "Food",
      "description": "Dinner at restaurant"
    }
    ```
- **Response**:
    - **Status**: `200 OK`
    - **Body**:
      ```json
      {
        "id": 1,
        "title": "Dinner",
        "amount": 20.0,
        "category": "Food",
        "description": "Dinner at restaurant",
        "date": "2025-03-06T18:30:00Z"
      }
      ```

---

### **5. Delete Expense**

- **URL**: `api/expenses/<int:pk>/delete/`
- **Method**: `DELETE`
- **Description**: Delete an expense by its ID.
- **Response**:
    - **Status**: `204 No Content`
    - **Body**: No content returned.

---
