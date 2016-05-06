from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic
from django.db.models import Avg, Count
from . import utils
from . import forms
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
        context['meals'] = models.DinnerPlanItem.objects.filter(plan=self.object)
        context['average_cost'] = models.DinnerPlan.objects.filter(cost__gt=0).aggregate(Avg('cost', ))['cost__avg']
        context['most_eaten'] = models.Recipe.objects.get(id=models.DinnerPlanItem.objects.values('recipe__id').annotate(num_recipes=Count('recipe_id')).latest('num_recipes')['recipe__id'])
        return context


class DinnerPlanDetails(generic.DetailView):
    template_name = 'foodplan/plan_details.html'

    def get_object(self, queryset=None):
        query = '%s-W%s' % (self.kwargs['year'], self.kwargs['week'])
        week_start = utils.get_start_date_from_year_and_week(query)
        model = models.DinnerPlan.objects.get(start_date=week_start)
        return model

    def get_context_data(self, **kwargs):
        context = super(DinnerPlanDetails, self).get_context_data()
        meals = models.DinnerPlanItem.objects.filter(plan=self.object)
        days = set([i for i in range(7)])
        not_added = days.difference(set([meals[i].day for i in range(len(meals))]))
        context.update({
            'meals': meals,
            'not_added': not_added
        })
        return context


class DinnerPlanCreate(generic.CreateView):
    model = models.DinnerPlan
    form_class = forms.DinnerPlanForm

    def get_success_url(self):
        return reverse('food:plan_edit', kwargs={'year': self.object.start_date.year,
                                                 'week': self.object.week})


class DinnerPlanEdit(generic.UpdateView):
    model = models.DinnerPlan
    fields = ['cost']

    def get_object(self, queryset=None):
        query = '%s-W%s' % (self.kwargs['year'], self.kwargs['week'])
        week_start = utils.get_start_date_from_year_and_week(query)
        model = models.DinnerPlan.objects.get(start_date=week_start)
        return model

    def get_context_data(self, **kwargs):
        context = super(DinnerPlanEdit, self).get_context_data(**kwargs)
        return context


class DinnerPlanItemAdd(generic.CreateView):
    model = models.Recipe
    form_class = forms.DinnerPlanItemAddForm
    template_name = 'foodplan/dinnerplanitem_add.html'
    # TODO: Success url to plan details

    def get_initial(self):
        query = '%s-W%s' % (self.kwargs['year'], self.kwargs['week'])
        week_start = utils.get_start_date_from_year_and_week(query)
        dinner_plan = get_object_or_404(models.DinnerPlan, start_date=week_start)
        return {'start_date': week_start}

    def get_success_url(self):
        # TODO: Not sure if safe to use kwargs here
        return reverse('food:plan_details', kwargs={'year': self.kwargs['year'],
                                                    'week': self.kwargs['week']})


class DinnerPlanItemEdit(generic.UpdateView):
    model = models.DinnerPlanItem
    fields = ['recipe', 'eaten']
    template_name = 'foodplan/dinnerplanitem_edit.html'

    def get_object(self, queryset=None):
        query = '%s-W%s' % (self.kwargs['year'], self.kwargs['week'])
        week_start = utils.get_start_date_from_year_and_week(query)
        model = models.DinnerPlanItem.objects.get(day=self.kwargs['day'], plan__start_date=week_start)
        return model

    def get_success_url(self):
        return reverse('food:plan_details', kwargs={'year': self.object.plan.year,
                                                    'week': self.object.plan.week})
