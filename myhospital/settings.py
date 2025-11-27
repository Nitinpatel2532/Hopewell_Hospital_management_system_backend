from pathlib import Path
import os

# ================================
# BASE DIR
# ================================
BASE_DIR = Path(__file__).resolve().parent.parent

# ================================
# SECRET KEY
# ================================
SECRET_KEY = os.environ.get("SECRET_KEY", "your-fallback-secret-key-for-dev")

# ================================
# DEBUG
# ================================
DEBUG = os.environ.get("DEBUG", "False") == "True"  # False in production

# ================================
# ALLOWED HOSTS
# ================================
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    ".onrender.com",  # Render backend domain
    "hopewell-hospital-management-system.vercel.app",  # Vercel frontend
]

# ================================
# INSTALLED APPS
# ================================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "corsheaders",

    # Your apps
    "superadmin",
    "hospital_management",
    "patient",
]

# ================================
# MIDDLEWARE (CORS must be first)
# ================================
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # MUST be first
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Static files
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ================================
# ROOT URLCONF
# ================================
ROOT_URLCONF = "myhospital.urls"

# ================================
# TEMPLATES
# ================================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ================================
# WSGI
# ================================
WSGI_APPLICATION = "myhospital.wsgi.application"

# ================================
# DATABASE
# ================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ================================
# PASSWORD VALIDATORS
# ================================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ================================
# INTERNATIONALIZATION
# ================================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ================================
# STATIC FILES
# ================================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ================================
# DEFAULT AUTO FIELD
# ================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ================================
# CORS SETTINGS
# ================================
CORS_ALLOWED_ORIGINS = [
    "https://hopewell-hospital-management-system.vercel.app",
]
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_CREDENTIALS = True

# ================================
# EMAIL SETTINGS
# ================================
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
