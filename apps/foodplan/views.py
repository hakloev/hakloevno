from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic
from django.db.models import Avg, Count
from django.core.exceptions import ObjectDoesNotExist
from . import utils
from . import forms
from . import models


class DinnerPlanObjectQueryMixin(object):
    """
    View mixin which locates dinner plan based on query
    Overrides get_object
    """

    def get_object(self, queryset=None):
        query = '%s-W%s' % (self.kwargs['year'], self.kwargs['week'])
        week_start = utils.get_start_date_from_year_and_week(query)
        model = models.DinnerPlan.objects.get(start_date=week_start)
        return model


class DinnerPlanIndex(generic.DetailView):
    model = models.DinnerPlan
    template_name = 'foodplan/index.html'
    context_object_name = 'plan'

    def get_object(self, queryset=None):
        # TODO: Add try/except
        plan = self.model.objects.current_plan()
        return plan

    def get_context_data(self, **kwargs):
        context = super(DinnerPlanIndex, self).get_context_data(**kwargs)
        most_eaten = None
        # TODO: Split this...
        try:
            most_eaten = models.Recipe.objects.get(id=models.DinnerPlanItem.objects.values('recipe__id').annotate(num_recipes=Count('recipe_id')).latest('num_recipes')['recipe__id'])
            average_cost = models.DinnerPlan.objects.filter(cost__gt=0).aggregate(Avg('cost', ))['cost__avg']
        except ObjectDoesNotExist as e:
            #  TODO: debug log here
            pass
        if not average_cost:
            average_cost = 'N/A'
        context['most_eaten'] = most_eaten
        context['average_cost'] = average_cost
        return context


class DinnerPlanDetails(DinnerPlanObjectQueryMixin, generic.DetailView):
    template_name = 'foodplan/plan_details.html'
    context_object_name = 'plan'

    def get_context_data(self, **kwargs):
        context = super(DinnerPlanDetails, self).get_context_data()
        meals = models.DinnerPlanItem.objects.filter(plan=self.object)
        days = set([i for i in range(7)])
        not_added = days.difference(set([meals[i].day for i in range(len(meals))]))
        context['not_added'] = not_added
        return context


class DinnerPlanCreate(generic.CreateView):
    model = models.DinnerPlan
    form_class = forms.DinnerPlanForm

    def get_success_url(self):
        return reverse('food:plan_details', kwargs={'year': self.object.year,
                                                    'week': self.object.week})


class DinnerPlanEdit(DinnerPlanObjectQueryMixin, generic.UpdateView):
    model = models.DinnerPlan
    fields = ['cost']

    def get_context_data(self, **kwargs):
        context = super(DinnerPlanEdit, self).get_context_data(**kwargs)
        return context


class DinnerPlanItemAdd(generic.CreateView):
    model = models.DinnerPlanItem
    template_name = 'foodplan/dinnerplanitem_add.html'

    def get_form_class(self):
        return forms.CustomAddPlanItemForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(DinnerPlanItemAdd, self).get_form_kwargs(**kwargs)
        if 'data' in kwargs:
            query = '%s-W%s' % (self.kwargs['year'], self.kwargs['week'])
            week_start = utils.get_start_date_from_year_and_week(query)
            plan = models.DinnerPlan.objects.get(start_date=week_start)
            instance = models.DinnerPlanItem(plan=plan)
            kwargs.update({'instance': instance})
        return kwargs

    def get_success_url(self):
        plan = models.DinnerPlan.objects.get(item=self.object)
        return reverse('food:plan_details', kwargs={'year': str(plan.year),
                                                    'week': str(plan.week)})



# class DinnerPlanItemAdd(generic.CreateView):
#     model = models.Recipe
#     form_class = forms.DinnerPlanItemAddForm
#     template_name = 'foodplan/dinnerplanitem_add.html'
#     TODO: Success url to plan details
    #
    # def get_initial(self):
    #     query = '%s-W%s' % (self.kwargs['year'], self.kwargs['week'])
    #     week_start = utils.get_start_date_from_year_and_week(query)
    #     dinner_plan = get_object_or_404(models.DinnerPlan, start_date=week_start)
    #     return {'start_date': week_start}
    #
    # def get_success_url(self):
    #     TODO: Not sure if safe to use kwargs here
        # return reverse('food:plan_details', kwargs={'year': self.kwargs['year'],
        #                                             'week': self.kwargs['week']})


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
