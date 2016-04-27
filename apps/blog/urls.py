from django.conf.urls import url

urlpatterns = [
    url(r'^$', None, name='index'),
    url(r'^archive/$', None, name='all_posts')
]
