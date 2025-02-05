import os
from pathlib import Path
import environ
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs

# Lade Umgebungsvariablen
load_dotenv()

# Django-Umgebung laden
env = environ.Env()
environ.Env.read_env()

# Basisverzeichnis der Anwendung
BASE_DIR = Path(__file__).resolve().parent.parent

# Sicherheitsvariablen
SECRET_KEY = env("SECRET_KEY", default="change-me")  # Fallback für Sicherheit
DEBUG = env.bool("DEBUG", default=True)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])

# Anwendungsdefinition
INSTALLED_APPS = [
    "shopping",
    "accounts",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "familyapp.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "familyapp.wsgi.application"

# ✅ Korrigierte Datenbankeinstellungen für NeonDB
DATABASE_URL = env("DATABASE_URL", default="")

if DATABASE_URL:
    tmpPostgres = urlparse(DATABASE_URL)
    query_params = parse_qs(tmpPostgres.query)

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': tmpPostgres.path.lstrip('/'),
            'USER': tmpPostgres.username,
            'PASSWORD': tmpPostgres.password,
            'HOST': tmpPostgres.hostname,
            'PORT': tmpPostgres.port or 5432,
            'OPTIONS': {
                'sslmode': query_params.get('sslmode', ['require'])[0],
                'options': query_params.get('options', [''])[0],
            }
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / "db.sqlite3",
        }
    }

# Passwortvalidierung
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Sprache und Zeitzone
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Statische Dateien
STATIC_URL = "static/"

# Primärer Schlüsseltyp
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Benutzerdefiniertes User-Modell
AUTH_USER_MODEL = 'accounts.CustomUser'