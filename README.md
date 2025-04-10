# 🛠️ Field Job Manager

A Django-based API for managing employees and their assigned jobs.

---

## 🚀 Features

- Create and manage users
- User authentication and authorization
- View/ Update/ Create/ Delete jobs
- Update job statuses: `To Do`, `In Progress`, `Done`
- View all jobs

---

## 📦 Tech Stack

- Python 3.10+
- Django 4.x
- SQLite (default)

---

## 🧑‍💻 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Niru-D/field-job-manager.git
cd your-repo-name
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Apply migrations

```bash
python manage.py migrate
```

### 4. Run the server

```bash
python manage.py runserver
```
