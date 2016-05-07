from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.DinnerPlanIndex.as_view(), name='index'),
    url(r'^plan/(?P<year>[0-9]{4})/week/(?P<week>\d+)/$', views.DinnerPlanDetails.as_view(), name='plan_details'),
    url(r'^plan/create/$', views.DinnerPlanCreate.as_view(), name='plan_create'),
    url(r'^plan/(?P<year>[0-9]{4})/week/(?P<week>\d+)/edit/$', views.DinnerPlanUpdate.as_view(), name='plan_edit'),
    url(r'^plan/(?P<year>[0-9]{4})/week/(?P<week>\d+)/edit/meal/(?P<day>[0-6])/edit/$', views.DinnerPlanItemUpdate.as_view(), name='plan_item_edit'),

    url(r'^recipe/all/', views.recipe_json, name='recipe_json')
    # url(r'^plan/(?P<year>[0-9]{4})/week/(?P<week>\d+)/edit/meal/add/$', views.DinnerPlanItemAdd.as_view(), name='plan_item_add'),

]
