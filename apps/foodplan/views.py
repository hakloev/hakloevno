from django.shortcuts import render
from django.views import generic
from django.db.models import Avg, Count
from datetime import datetime
from . import utils
from . import models


class DinnerPlanIndex(generic.DetailView):
    template_name = 'foodplan/index.html'
    context_object_name = 'newest_plan'

    def get_object(self, queryset=None):
        newest_plan = models.DinnerPlan.objects.current_plan()
        if not newest_plan:
            return models.DinnerPlan.objects.latest()
        return newest_plan

    def get_context_data(self, **kwargs):
        context = super(DinnerPlanIndex, self).get_context_data()
        context['average_cost'] = models.DinnerPlan.objects.aggregate(Avg('cost'))['cost__avg']
        context['most_eaten'] = models.Recipe.objects.get(id=models.DinnerPlanItem.objects.values('recipe__id').annotate(num_recipes=Count('recipe_id')).latest('num_recipes')['recipe__id'])
        return context


class DinnerPlanDetails(generic.DetailView):
    template_name = 'foodplan/plan_details.html'

    def get_object(self, queryset=None):
        query = '%s-W%s' % (self.kwargs['year'], self.kwargs['week'])
        week_start = utils.get_start_date_from_year_and_week(query)
        model = models.DinnerPlan.objects.get(start_date=week_start)
        return model


