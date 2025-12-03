"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path
from django.views.generic import RedirectView

app_name = "api"  # Required for reverse urls, do not remove.

v1_urls = [
    # This is just an example that will become `/{{app_name}}/v1/nothing`
    path("nothing/", RedirectView.as_view(url="/nothing/"), name="nothing"),
]

# This is what the main project will include in the root urls.
urlpatterns = [
    path("v1/", include(v1_urls)),
]


# TODO (rochacbruno): Add default implementation for health URLS
