"""# The main settings for {{project_name}}.

## On this module

1. Default Settings (regular django settings)
2. Dynaconf instrumentation that loads external settings including
[DAB](https://github.com/ansible/django-ansible-base) defaults

## Loading order

1. Project defaults as defined in the first section of this file.
2. DAB defaults.
3. Application defaults.
   - for each `app/settings.py` in `apps` directory.
4. DAB conditional settings.
   - Loaded based on what is on current INSTALLED_APPS, MIDDLEWARES etc
5. Overrides from standard paths.
   - /etc/ansible-automation-platform/{service_name}/
6. Overrides from environment variables prefixed with {SERVICE_NAME}.
7. Post loading hooks registered on any Python file loaded before.

## Overrides

> [!NOTE]
> To override defaults define variables on each `apps`/app_name/settings.py.
> To override settings on environments use the override path `/etc/...`
> or set environment varibles prefixed with `{{project_name | upper }}_`.
> The environment variables can also be used on development environments
> by adding a `.env` file to the root of the project or creaeting a
> `settings.local.py`

## Inspecting settings and troubleshooting

To examine the loading history of the settings loading mechanism.

```bash
# Export the Django Settings Module Variable
export DJANGO_SETTINGS_MODULE=platform_service_example.settings

# The whole history
uv run dynaconf inspect -m debug -f yaml

# Inspect a variable
uv run dynaconf inspect -k VARIABLE
```

## Default variables
"""

from pathlib import Path

from ansible_base.lib.dynamic_config import (
    export,
    factory,
    load_dab_settings,
    load_envvars,
    load_standard_settings_files,
)
from dynaconf.loaders import execute_instance_hooks

BASE_DIR = Path(__file__).resolve().parent.parent
"""Build paths inside the project like this: BASE_DIR / 'subdir'"""

SECRET_KEY = "django-insecure-k^a&fnx3ulh*d2nl%q680o+xkr^5o+c$5=lzo7vd-7=#qmadg("
"""SECURITY WARNING: keep the secret key used in production secret!"""

DEBUG = True
"""SECURITY WARNING: don't run with debug turned on in production!"""

ALLOWED_HOSTS = []
"""List of allowed hosts"""

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
"""List of installed apps"""

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
"""List of middleware classes"""


ROOT_URLCONF = "platform_service_example.urls"
"""URL configuration for platform_service_example project."""


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
"""List of template configurations"""


WSGI_APPLICATION = "platform_service_example.wsgi.application"
"""WSGI application configuration"""

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
"""Database configuration"""

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
"""Password validation configuration"""

LANGUAGE_CODE = "en-us"
"""Language code for this installation."""

TIME_ZONE = "UTC"
"""Time zone for this installation."""

USE_I18N = True
"""Internationalization configuration"""

USE_TZ = True
"""Time zone configuration"""

STATIC_URL = "static/"
"""Static files configuration"""

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
"""Default primary key field type"""

FOO = "original"
"""Example variable"""

default_variables = {k: v for k, v in locals().items() if k.isupper()}
"""Variables from this module locals that will be passed to Dynaconf"""

## --- End Default Settings | Start Dynaconf instrumentation --- #

# TODO(rochacbruno): Add Validators
# TODO(rochacbruno): Read local development files

DYNACONF = factory(__name__, "EXAMPLE", add_dab_settings=False, **default_variables)
"""Dynaconf instance that comes with settings injected by DAB"""

apps_dir = Path(BASE_DIR / "apps")
"""The directory where the django apps will be discovered from"""

if apps_dir.exists():
    all_apps = [app for app in apps_dir.iterdir() if Path(app / "apps.py").exists()]
    apps_import_paths = [f"apps.{app.name}" for app in all_apps]
    DYNACONF.set("INSTALLED_APPS", f"@merge {apps_import_paths}")
    for app in all_apps:
        DYNACONF.load_file(app / "settings.py", run_hooks=False)

load_dab_settings(DYNACONF)
"""DAB default and DAB conditionals that needs to load after project and app settings."""

load_standard_settings_files(DYNACONF)
"""Load settings overrides from the standard paths, this is the **user** settings."""

load_envvars(DYNACONF)
"""Load envvars at the end to allow them to override everything loaded so far"""

if DYNACONF.get("DEBUG"):
    DYNACONF.set("INSTALLED_APPS", "@merge django_extensions")

# TODO(rochacbruno): Move this internally to DAB as a helper method.
execute_instance_hooks(
    DYNACONF,  # type: ignore
    "post",
    [
        _hook
        for _hook in DYNACONF._post_hooks
        if getattr(_hook, "_dynaconf_hook", False) is True and not getattr(_hook, "_called", False)
    ],
)
"""This executes the hooks deferred from application settings to execute later."""

export(__name__, DYNACONF)
"""Update django.conf.settings with DYNACONF keys."""

## --- End Settings | After this line only post validation can happen --- #
