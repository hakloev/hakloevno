from django.shortcuts import render
from django.views import generic
from datetime import datetime, timedelta
from django.db.models import Count
from . import models


class DinnerPlanIndex(generic.ListView):
    model = models.DinnerPlan
    template_name = 'foodplan/index.html'

    def get_context_data(self, **kwargs):
        context = super(DinnerPlanIndex, self).get_context_data()
        context['most'] = models.Recipe.objects.get(id=models.DinnerPlanItem.objects.values('recipe__id').annotate(num_recipes=Count('recipe_id')).latest('num_recipes')['recipe__id'])
        return context

class DinnerPlanDetails(generic.DetailView):
    template_name = 'foodplan/plan_details.html'

    def get_object(self, queryset=None):
        query = '%s-W%s' % (self.kwargs['year'], self.kwargs['week'])
        week_start = datetime.strptime(query + '-1', '%Y-W%W-%w')  # Get start_date of week from kwargs
        model = models.DinnerPlan.objects.get(start_date=week_start)
        return model


