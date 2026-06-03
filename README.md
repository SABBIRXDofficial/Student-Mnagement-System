# EduBright Student Management System
**Stack:** Django 4.2 · MySQL · Vanilla HTML/CSS · Python 3.10+

---

## Full User Flow

```
Homepage (/)
  ├── Login (/login/)  ──────────────────► Dashboard (/dashboard/)
  │                                              │
  └── Register (/register/) → Login             ├── Students   (/students/)
                                                 ├── Courses    (/courses/)
                                                 ├── Fees       (/fees/)
                                                 ├── Exams      (/exams/)
                                                 ├── Users      (/users/)
                                                 ├── Roles      (/roles/)
                                                 ├── Permissions(/permissions/)
                                                 └── Login Recs (/logins/)
```

---

## Quick Setup (5 steps)

### 1. Create & activate virtual environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create MySQL database
```sql
-- In MySQL Workbench or mysql CLI:
CREATE DATABASE student_management_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. Configure environment
```bash
# Edit .env with your MySQL password:
DB_PASSWORD=your_mysql_password
```

### 5. Run migrations & start server
```bash
python manage.py makemigrations core
python manage.py migrate
python manage.py runserver
```

Open **http://127.0.0.1:8000** — you'll see the homepage.

---

## Create First Admin Login

After migrations, run this in Django shell:
```bash
python manage.py shell
```
```python
from core.models import Role, User, Login
from django.contrib.auth.hashers import make_password

role = Role.objects.create(role_name='Admin', role_desc='Full access')
user = User.objects.create(user_name='Admin', user_email='admin@school.com')
Login.objects.create(
    login_username='admin',
    user_password=make_password('admin123'),
    login_role=role,
    user=user
)
print("Done! Login with: admin / admin123")
```

Then go to **http://127.0.0.1:8000/login/** and log in.

---

## Project Structure
```
student_management/
├── manage.py
├── requirements.txt
├── .env                    ← your config (DB password etc.)
├── sms/                    ← Django project package
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── core/                   ← Main Django app
│   ├── models.py           ← All DB models (ER diagram)
│   ├── views.py            ← All view logic
│   ├── urls.py             ← All URL routes
│   ├── forms.py            ← Django forms
│   └── admin.py            ← Django admin config
├── templates/
│   ├── home.html           ← Public homepage
│   ├── sms_base.html       ← Base for all SMS pages (sidebar)
│   └── core/
│       ├── login.html
│       ├── register.html
│       ├── dashboard.html
│       ├── student_list.html
│       ├── course_list.html
│       ├── fee_list.html
│       ├── exam_list.html
│       ├── user_list.html
│       ├── role_list.html
│       ├── permission_list.html
│       ├── login_list.html
│       ├── form.html       ← Reusable edit form
│       └── confirm_delete.html
├── static/
│   ├── css/sms.css         ← All SMS styling
│   └── images/             ← logo, library, playground, canteen
└── database/
    └── schema.sql          ← Raw MySQL schema (optional)
```

---

## URL Reference
| URL | Page | Auth Required |
|-----|------|--------------|
| `/` | Homepage | ✗ Public |
| `/login/` | Login | ✗ Public |
| `/register/` | Register | ✗ Public |
| `/logout/` | Logout | — |
| `/dashboard/` | Dashboard | ✓ |
| `/students/` | Student CRUD | ✓ |
| `/courses/` | Course CRUD | ✓ |
| `/fees/` | Fee CRUD | ✓ |
| `/exams/` | Exam CRUD | ✓ |
| `/users/` | User CRUD | ✓ |
| `/roles/` | Role CRUD | ✓ |
| `/permissions/` | Permission CRUD | ✓ |
| `/logins/` | Login Records | ✓ |
| `/admin/` | Django Admin | ✓ Superuser |
