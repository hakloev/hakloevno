from django.shortcuts import render
from django.views import generic
from . import models


class FoodPlanIndex(generic.ListView):
    model = models.WeekPlanRecipes
    template_name = 'foodplan/index.html'

    def get_context_data(self, **kwargs):
        context = super(FoodPlanIndex, self).get_context_data(**kwargs)
        context['food_list'] = models.WeekPlanRecipes.objects.all()
        return context
