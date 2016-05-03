from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.DinnerPlanIndex.as_view(), name='index'),
    url(r'^(?P<year>[0-9]{4})/week/(?P<week>\d+)/$', views.DinnerPlanDetails.as_view(), name='plan_details')
]
