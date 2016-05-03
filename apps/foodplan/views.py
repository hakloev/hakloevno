from django.shortcuts import render
from django.views import generic
from . import models


class FoodPlanIndex(generic.ListView):
    model = models.DinnerPlanItem
    template_name = 'foodplan/index.html'
    queryset = models.DinnerPlanItem.objects.all()

    # def get_context_data(self, **kwargs):
    #     context = super(FoodPlanIndex, self).get_context_data(**kwargs)
    #     context['food_list'] = models.WeekPlanRecipes.objects.all()
    #     return context
