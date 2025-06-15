# Leave Management System (Django)

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)

A comprehensive web-based solution for automating leave request and approval processes in organizations.

## ✨ Key Features

### 👨‍💼 Employee Features
- 📝 Intuitive leave application interface
- 🔍 Transparent leave balance tracking
- 📅 Easy form submission with leave type dropdowns
- 📊 Application history review

### 👩‍💼 Admin Features
- ✅ Complete leave workflow management (approval/rejection)
- 👥 Employee management portal
- 🔐 Secure user account provisioning
- 📈 Comprehensive dashboard and reporting

## 🛠️ Technical Stack

| Component               | Technology Used                          |
|-------------------------|-----------------------------------------|
| Backend Framework       | Django 4.x                              |
| Frontend                | HTML5, CSS3, Bootstrap 5                |
| Database                | SQLite (Development)                    |
| Authentication          | Django's built-in auth system           |
| Form Handling           | django-crispy-forms, widget-tweaks      |
| Image Processing        | Pillow                                  |
                  

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/saumyasaanvi/LeaveMgmt-Django.git
cd LeaveMgmt-Django
```
2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Run migrations:
```bash
python manage.py migrate
```
5. Create superuser (for admin access):
```bash
python manage.py createsuperuser
```
6. Run development server:
```bash
python manage.py runserver
```
## 🤝 Contributing
Pull requests are welcome! Please open an issue first to discuss proposed changes.

## 📄 License
MIT

Developed by Saumya Saanvi ❤️
