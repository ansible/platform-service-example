"""
Service Default Settings
"""

# from django.conf import settings
# django settings is available here but is read only
# to set variables simply declare them.
# use dynaconf merging syntax.

from dynaconf import post_hook

FOO = "override from apps/api"


@post_hook
def foo(config):
    return {"FOO": "batata"}
