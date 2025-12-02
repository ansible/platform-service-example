"""Top level settings file for all apps.

The settings here overrides any setting previously loaded
from the {{project_name}}.settings

In order to merge wit previously defined setting
use Dynaconf merging markers such as:
@merge, @merge_unique, @insert on string values and
`dynaconf_merge` or `dynaconf_merge_unique` on data structures.

The settings defined here can be overridden from
each app own settings.py, environment local override files and
environment variables.
"""

INSTALLED_APPS = [
    "dynaconf_merge_unique",  # DO NOT REMOVE THIS
    "apps.api",
]
