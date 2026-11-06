Logistics

A Django-based web application for Logis Kenya freight and transportation services.

Features

- Responsive design built with Bootstrap 5
- Pages: Home, About, Services, Service Details, Pricing, Contact, and Quote Request
- Interactive quote and contact inquiry forms

Template Structure & `base.html`

All pages use `logis/templates/base.html` as the master layout:
- Shared elements:Holds the `<head>`, navigation bar, footer, and static assets (CSS & JS).
- Page inheritance:Child pages use `{% extends 'base.html' %}` and place their unique content inside `{% block content %}` without repeating layout code.

Tech Stack

- **Backend:** Python, Django
- **Database:** SQLite
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5

Setup and Running

1. **Activate the virtual environment:**
   ```powershell
   .\venv\Scripts\activate
   ```

2. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

3. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

4. Open your browser at `http://127.0.0.1:8000/`.

Running Tests

```bash
python manage.py test
```
