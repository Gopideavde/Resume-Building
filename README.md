# ResumePro 🚀

ResumePro is a premium, modern SaaS platform for building professional resumes with ease. Featuring dynamic templates, premium access via Razorpay, real-time preview, and full user dashboard capabilities.

## ✨ Features
- **Dynamic Template Explorer**: Browse free and premium resume templates with live previews.
- **Resume Builder Engine**: Build, manage, and edit personal information, education, experience, and skills in a seamless flow.
- **Premium Access Control**: Secure payment integration via Razorpay for unlocking premium templates.
- **User Dashboards**: Dedicated user profiles, resume tracking, and account management.
- **Powerful Admin Portal**: Fully customized Django Admin for managing site settings, dynamic branding, users, templates, and audit logs.
- **Persistent Media**: Cloudinary integration for scalable logo, favicon, and profile photo storage.

## 🛠 Technology Stack
- **Backend Framework**: Django 5.1 & Python 3.14
- **Database**: PostgreSQL (Production) / MySQL (Clever Cloud) / SQLite (Local fallback)
- **Frontend**: HTML5, CSS3, Vanilla JS, Bootstrap 5, custom AOS micro-animations.
- **Payment Gateway**: Razorpay (Test Mode & Live Ready)
- **Cloud Storage**: Cloudinary & WhiteNoise (Static Files)
- **Deployment**: Configured for Render via `render.yaml` and Gunicorn WSGI.

## 📁 Project Architecture
- `core/`: Global models (SiteSettings for dynamic branding) and context processors.
- `accounts/`: Custom `AbstractUser` model (email authentication) and profiles.
- `resumes/`: The core Resume builder engine, parsing experience, education, and skills.
- `templates_app/`: Template definitions, categories, and premium configurations.
- `payments/`: Razorpay checkout flow, signature verification, and transaction logging.
- `dashboard/`: User-facing resume management portal.
- `admin_panel/`: Specialized views for administration tracking.

## 🚀 Local Development Setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd resumepro
```

### 2. Create the Virtual Environment
```bash
python -m venv env
# Windows:
env\Scripts\activate
# Mac/Linux:
source env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables (`.env`)
Create a `.env` file in the root directory. **Never commit this file.** Use the following template:

```env
# Security
DEBUG=True
SECRET_KEY=your_development_secret_key_here
ALLOWED_HOSTS=*

# Database (MySQL / Clever Cloud)
DB_ENGINE=mysql
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=3306

# Storage (Cloudinary)
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# Payments (Razorpay)
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_secret
```

### 5. Run Migrations & Collect Static
```bash
python manage.py migrate
python manage.py collectstatic
```

### 6. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 7. Run Server
```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## 🔒 Security Notes
This project utilizes modern Django security features. When deployed with `DEBUG=False`, it automatically enforces:
- HTTP Strict Transport Security (HSTS)
- Secure Session & CSRF Cookies
- XSS and Content Type protections
All API secrets and passwords must be injected via environment variables on your deployment platform (e.g., Render).

---
© 2026 ResumePro. Built for modern careers.
