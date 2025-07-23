# Internal Asset Management System 🏢💻📦

A Django-based web application to track and manage company assets such as computers, routers, phones, and more. Originally developed for Gmobile LLC to digitize workflows and reduce manual labor.

> 🏆 Helped reduce company expenditures by **95%**
> 🏅 Awarded **Best Employee of the Company** in 2020 for this system

---

## 🧩 Features

- Asset registration and categorization
- Track asset location, status, and user
- Admin panel for editing and reporting
- WebSocket support for real-time updates (if enabled)
- Secure login and access control for internal teams

---

## 🛠️ Tech Stack

- Python 3.x
- Django
- MySQL
- HTML / CSS / JavaScript
- WebSocket (Django Channels or similar)

---

## 🚀 Installation

```bash
git clone https://github.com/batbyr-hub/asset.git
cd asset
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
