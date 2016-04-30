from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$', views.login_override, name='login'),
    url(r'^logout/$', views.logout_override, name='logout')
]