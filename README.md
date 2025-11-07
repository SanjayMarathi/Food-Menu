# 📸 Screenshots

---

### 🛒 Customer Menu Page
<p align="center">
  <img src="output/customerMenu.png" width="700" alt="Item Update" />
</p>
Displays the full digital menu that customers see after scanning the QR code.

---

### ✏️ Update Item Page (Staff)
<p align="center">
  <img src="output/itemUpdate.png" width="700" alt="Item Update" />
</p>
Staff can update food items, change availability, and edit pricing.

---

### 🔐 Login Page
<p align="center">
  <img src="output/login.png" width="700" alt="Login" />
</p>
Secure staff login required to access management dashboard.

---

### 📱 QR Code for Tables
<p align="center">
  <img src="output/qrfortables.png" width="700" alt="QR for Tables" />
</p>
Each table receives a unique QR code for ordering.

---

### 🧾 Registration Page
<p align="center">
  <img src="output/registration.png" width="700" alt="Registration" />
</p>
Staff can register new accounts if allowed.

---

### 🧑‍🍳 Staff Dashboard
<p align="center">
  <img src="output/staffdashboard.png" width="700" alt="Staff Dashboard" />
</p>
Central hub showing active orders, statuses, and actions.

---

### 🍽️ Staff Menu Management
<p align="center">
  <img src="output/staffMenu.png" width="700" alt="Staff Menu" />
</p>
Interface for staff to add or edit menu items.

---

### 👤 Staff Profile Page
<p align="center">
  <img src="output/staffprofile.png" width="700" alt="Staff Profile" />
</p>
Displays staff account information and settings.

---

---

### 🛒 Customer Menu Page
<p align="center">
  <img src="output/customerMenu.png" width="700"/>
</p>

Displays the full digital menu that customers see after scanning the QR code.

---

### ✏️ Update Item Page (Staff)
<p align="center">
  <img src="output/itemUpdate.png" width="700"/>
</p>

Staff can update food items, change details, and update pricing.

---

### 🔐 Login Page
<p align="center">
  <img src="output/login.png" width="700"/>
</p>

Staff login required to access the dashboard.

---

### 📱 QR Code for Tables
<p align="center">
  <img src="output/qrfortables.png" width="700"/>
</p>

Each table receives a unique QR code for ordering.

---

### 🧾 Registration Page
<p align="center">
  <img src="output/registration.png" width="700"/>
</p>

Staff can register an account if allowed.

---

### 🧑‍🍳 Staff Dashboard
<p align="center">
  <img src="output/staffdashboard.png" width="700"/>
</p>

Displays active orders, statuses, and actions.

---

### 🍽️ Staff Menu Management
<p align="center">
  <img src="output/staffMenu.png" width="700"/>
</p>

Interface to manage all menu items.

---

### 👤 Staff Profile Page
<p align="center">
  <img src="output/staffprofile.png" width="700"/>
</p>

Displays staff account information.

---

---

# 🍽️ FoodApp – QR Based Digital Menu & Ordering System

FoodApp is a modern Django project that provides:
✅ A QR-based digital menu for customers  
✅ A simple order-tracking panel for staff  
✅ Menu management (CRUD)  
✅ Session-based cart system  

This is **not a restaurant management system** — it is a **lightweight food ordering system** for tables using QR codes.

---

# ✅ Key Features

## 👨‍🍳 Staff / Admin Features
```
• Secure staff login  
• Add, edit, delete menu items  
• Upload item images  
• Toggle item availability  
• Track active orders  
• Update order status  
• Generate QR codes for tables  
• View revenue & top-selling items  
```

---

## 📱 Customer Features
```
• Scan QR code → instantly open menu  
• Browse items with images  
• Tap item card → view description  
• Add items to cart (session-based)  
• Place order quickly  
• Auto-detected table number  
```

---

# 💻 Technology Stack
```
Backend: Django 5  
Frontend: Tailwind CSS (CDN)  
Database: SQLite / MySQL  
QR Code: qrcode + Pillow  
Deployment: Gunicorn / PythonAnywhere  
```

---

# ⚙️ Setup & Installation

### 1️⃣ Clone Repository
```
git clone https://github.com/SanjayMarathi/Food-Menu.git
cd mysite
```

---

### 2️⃣ Create & Activate Virtual Environment
```
python -m venv venv
```

**Windows**
```
.\venv\Scripts\activate
```

**macOS/Linux**
```
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies
```
pip install -r requirements.txt
```

If requirements.txt is missing:
```
pip install django gunicorn qrcode pillow
```

---

### 4️⃣ Apply Migrations
```
python manage.py makemigrations myapp
python manage.py migrate
```

---

### 5️⃣ Create Superuser
```
python manage.py createsuperuser
```

---

### 6️⃣ Run Server
```
python manage.py runserver
```

App opens at:

```
http://127.0.0.1:8000/
```

---

# 🚦 Usage Guide

## ✅ Staff / Admin Workflow
```
1. Login → /users/login/
2. Manage Menu → Add / Edit / Delete items
3. Generate Table QR → Staff Dashboard
4. Track Customer Orders (Pending → Preparing → Completed)
5. View revenue and best-seller stats
```

Dashboard:
```
http://127.0.0.1:8000/management/dashboard/
```

---

## ✅ Customer Workflow
```
1. Scan table QR code
2. Browse menu for that table
3. Add items to cart
4. Place order
5. Order appears instantly on staff dashboard
```

Example table link:
```
http://127.0.0.1:8000/table/101/
```

---

# ✅ Project Structure
```
FoodApp/
│── myapp/
│   ├── templates/
│   │   ├── menu.html
│   │   ├── cart.html
│   │   ├── staff_dashboard.html
│   │   ├── item_detail.html
│   │   ├── how_to_use.html
│   │   ├── create_item.html
│   │   └── login.html / register.html
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── qr_utils.py
│
│── static/
│── manage.py
│── requirements.txt
```
---

# ✅ Author
```
Developed by: Sanjay Marathi
GitHub: https://github.com/SanjayMarathi
```

---

