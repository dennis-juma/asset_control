from .base import *
import os
DEBUG = False

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="assets.sunking.com",
    cast=lambda v: [s.strip() for s in v.split(",")],
)

SECURE_SSL_REDIRECT = config(
    "SECURE_SSL_REDIRECT",
    default=True,
    cast=bool,
)

SESSION_COOKIE_SECURE = config(
    "SESSION_COOKIE_SECURE",
    default=True,
    cast=bool,
)

CSRF_COOKIE_SECURE = config(
    "CSRF_COOKIE_SECURE",
    default=True,
    cast=bool,
)

SECURE_HSTS_SECONDS = config(
    "SECURE_HSTS_SECONDS",
    default=31_536_000,
    cast=int,
)

SECURE_HSTS_INCLUDE_SUBDOMAINS = config(
    "SECURE_HSTS_INCLUDE_SUBDOMAINS",
    default=True,
    cast=bool,
)

SECURE_HSTS_PRELOAD = config(
    "SECURE_HSTS_PRELOAD",
    default=True,
    cast=bool,
)

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]