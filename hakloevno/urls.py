"""hakloevno URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import TemplateView

from .views import home_files, index

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('apps.authentication.urls', namespace='auth')),
    url(r'^markdown/', include('django_markdown.urls')),
    url(r'^(?P<file_name>(robots.txt)|(humans.txt))$', home_files, name="home-files"),
    url(r'^blog/', include('apps.blog.urls', namespace='blog')),
    url(r'^food/', include('apps.foodplan.urls', namespace='food'))
]
