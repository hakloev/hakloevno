from django.conf.urls import url
from . import views, feed

urlpatterns = [
    url(r'^$', views.BlogIndex.as_view(), name='index'),
    url(r'^post/(?P<slug>\S+)/$', views.BlogPostDetail.as_view(), name='blog_post'),
    url(r'^feed/$', feed.LatestPosts(), name='feed'),
]
