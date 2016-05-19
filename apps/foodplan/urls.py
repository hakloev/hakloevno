from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.DinnerPlanIndex.as_view(), name='index'),
    url(r'^plan/(?P<year>[0-9]{4})/week/(?P<week>\d+)/$', views.DinnerPlanDetails.as_view(), name='plan_details'),
    url(r'^plan/create/$', views.DinnerPlanCreate.as_view(), name='plan_create'),
    url(r'^plan/(?P<year>[0-9]{4})/week/(?P<week>\d+)/edit/$', views.DinnerPlanUpdate.as_view(), name='plan_update'),
    url(r'^plan/history/$', views.DinnerPlanList.as_view(), name='plan_history'),

    url(r'^recipe/list/$', views.RecipesIndex.as_view(), name='recipe_list'),
    url(r'^recipe/add/$', views.RecipeCreate.as_view(), name='recipe_create'),
    url(r'^recipe/all/$', views.recipe_json, name='recipe_json'),

    url(r'^meal/edit/$', views.meal_edit_eaten, name='meal_edit_eaten')
]
