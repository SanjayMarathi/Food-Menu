# 📸 Screenshots

(Add your screenshots here)

Example:
![Dashboard Screenshot](path/to/dashboard.png)
![Menu Screenshot](path/to/menu.png)

---

# 🍽️ FoodApp: Hotel Menu & Order Tracking System

FoodApp is a modern Django application that provides QR-based digital menus for customers and a real-time order tracking system for hotel/restaurant staff.

---

# ✅ Key Features

## 👨‍🍳 Staff / Admin Features
- Secure login (staff only)
- Full menu CRUD management
- Toggle item availability
- Generate QR codes for tables
- Real-time order dashboard
- Update order status (Pending → Preparing → Completed/Paid)
- View detailed order breakdown
- Revenue analytics (total orders, revenue, top-selling items)

---

## 📱 Customer Features
- Scan QR to access digital menu
- Add items to cart (session-based)
- Quick order placement
- Table auto-detected from QR
- Mobile-optimized UI using TailwindCSS

---

# 💻 Technology Stack

- Django 5.0.7  
- SQLite  
- Tailwind CSS (CDN)  
- qrcode + Pillow  
- Gunicorn  

---

# ⚙️ Setup & Installation

## 1️⃣ Clone Repository

git clone <your-repository-url>
cd mysite
## 2️⃣ Create & Activate Virtual Environment
bash
Copy code
python -m venv venv
Windows:
bash
Copy code
.\venv\Scripts\activate
macOS/Linux:
bash
Copy code
source venv/bin/activate
## 3️⃣ Install Dependencies
bash
Copy code
pip install -r requirements.txt
If requirements.txt is missing:

bash
Copy code
pip install django gunicorn qrcode pillow
## 4️⃣ Apply Migrations
bash
Copy code
python manage.py makemigrations myapp
python manage.py migrate
## 5️⃣ Create Superuser
bash
Copy code
python manage.py createsuperuser
## 6️⃣ Run Server
bash
Copy code
python manage.py runserver
App available at:

cpp
Copy code
http://127.0.0.1:8000/
🚦 Usage Guide
✅ Staff / Admin Workflow
Login: /users/login/

Menu Management: http://127.0.0.1:8000/management/

Generate QR Codes: http://127.0.0.1:8000/management/dashboard/

Track & update orders

View revenue reports

✅ Customer Workflow
Scan QR or open link such as:
http://127.0.0.1:8000/table/101/

Browse menu & add items to cart

Place order → visible instantly in staff dashboard

