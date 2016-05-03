from django.shortcuts import render
from django.views import generic
from datetime import datetime, timedelta
from . import models


class DinnerPlanIndex(generic.ListView):
    model = models.DinnerPlan
    template_name = 'foodplan/index.html'


class DinnerPlanDetails(generic.DetailView):
    template_name = 'foodplan/plan_details.html'

    def get_object(self, queryset=None):
        query = '%s-W%s' % (self.kwargs['year'], self.kwargs['week'])
        week_start = datetime.strptime(query + '-1', '%Y-W%W-%w')  # Get start_date of week from kwargs
        model = models.DinnerPlan.objects.get(start_date=week_start)
        return model


