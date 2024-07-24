import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    DEBUG = True

    WTF_CSRF_ENABLED = False 

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(BASE_DIR / 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CORS_ALLOWED_ORIGINS = ['*']
    CORS_ALLOW_HEADERS = [
        'accept',
        'accept-encoding',
        'authorization',
        'content-type',
        'dnt',
        'origin',
        'user-agent',
        'x-csrftoken',
        'x-requested-with',
    ]