# Inventory Management System

![Inventory Banner](img/download.webp)

A full-featured **Inventory Management System** built with **Python** and **Tkinter**, utilizing **SQLite** for database operations. This desktop application allows users to manage employees, products, suppliers, sales, categories, and generate detailed billing.

---

## 🌟 Features

### 🔐 Authentication

* Employee login with role-based access (Admin & Employee).

### 🧑 Employee Management

* Add, update, delete, and search employees.

### 🧾 Billing System

* Cart functionality with live product stock updates.
* Dynamic bill generation with discount calculation.
* Print/save customer bills.

### 📦 Product Management

* Add, update, delete products with categories and supplier linking.
* Stock status handling.

### 📊 Dashboard

* Live statistics for total employees, products, suppliers, categories, and sales.

### 📂 Category & Supplier Management

* Add/delete categories and suppliers.

### 🧮 Calculator

* In-built calculator for quick calculations during billing.

---

## 🛠️ Technologies Used

| Component      | Technology Used          |
| -------------- | ------------------------ |
| Language       | Python 3                 |
| GUI Library    | Tkinter                  |
| DBMS           | SQLite3                  |
| Image Handling | PIL (Pillow)             |
| File System    | OS, Tempfile, Subprocess |

---

## 🗃️ Project Structure

```
Inventory-Management-System/
├── billing.py           # Billing module
├── category.py          # Manage product categories
├── createDB.py          # Initialize database
├── dashboard.py         # Admin dashboard
├── employee.py          # Employee management
├── functions.py         # Shared utilities
├── main.py              # Login system
├── product.py           # Product management
├── sales.py             # Sales tracking
├── supplier.py          # Supplier management
├── sms.db               # SQLite database file
├── bill/                # Saved customer bills
└── img/                 # Images used in the UI
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/kishandev2509/Inventory-Management-System.git
cd Inventory-Management-System
```

### 2. Install Required Packages

Make sure `pillow` is installed:

```bash
pip install pillow
```

### 3. Run the Application

```bash
python main.py
```

Upon first run, the database `sms.db` will be initialized automatically.

---

## 🔒 Default Admin Credentials

```
Employee ID: 1
Password: password
User Type: Admin
```

---

## 📋 Use Cases

* Small-scale retail store
* Pharmacy or departmental billing system
* POS system for inventory and sales

---

## 📸 Screenshots

(You may add GUI screenshots here of the dashboard, billing page, employee form, etc.)

---

## 📝 Future Improvements

* PDF export for bills
* Dark mode support
* Network-based database sharing (multi-user support)

---

## 🙏 Credits

This project was created and is maintained by **Kishan Dev**.

Special thanks to open-source communities and Python resources that inspired this project.

---
