"""API app default settings.

This file defines settings to be loaded on top of
platform services framework default settings.

Django settings are available for consulting only
Do not asign directly to django settings here
as it is in the middle of loading.

```python
from django.conf import settings
if settings.DEBUG:
    # BAD (attempt to mutate a partially loaded django settings)
    settings.MY_VAR = "some value"
    # GOOD (simply define an upper variable, this will become a setting)
    MY_VAR = "some value"
```

In order to change or merge existing variable use Dynaconf merging markers
those are traceable and safe.

```python
INSTALLED_APPS = "@merge new_app"
INSTALLED_APPS = "@insert 0 new_app"
DATABASES__default__OPTIONS__thing = True
```

Varibles defined here are loaded before DAB, user overrides and envvars,
so any variable from here can be overriden later, in order to postpone
the assignment of a variable defer a post_hook that runs ar the end.

```python
from dynaconf import post_hook
@post_hook
def foo(current_settings: dict):
    return {"MYVAR": "value that loads later and cannot be overriden"}
```
"""

FOO = "FOO override from apps/api"
"""Docstrings below variables are used to build the docs."""
