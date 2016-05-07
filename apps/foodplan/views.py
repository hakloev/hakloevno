from django.shortcuts import render, get_object_or_404, redirect
from django.http.response import JsonResponse
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
    template_name = 'foodplan/create_plan.html'
    form_class = forms.DinnerPlanForm

    def get_context_data(self, **kwargs):
        context = super(DinnerPlanCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = forms.ItemFormSet(self.request.POST)
        else:
            context['formset'] = forms.ItemFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.object.get_absolute_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class DinnerPlanUpdate(DinnerPlanObjectQueryMixin, generic.UpdateView):
    template_name = 'foodplan/create_plan.html'
    form_class = forms.DinnerPlanForm
    context_object_name = 'plan'

    def get_form(self, form_class=None):
        form = super(DinnerPlanUpdate, self).get_form(form_class=form_class)
        del form.fields['start_date']
        return form

    def get_context_data(self, **kwargs):
        context = super(DinnerPlanUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = forms.ItemFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = forms.ItemFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.object.get_absolute_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class DinnerPlanItemUpdate(generic.UpdateView):
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

"""
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

"""


def recipe_json(request):
    return JsonResponse([r.to_json() for r in models.Recipe.objects.all()], safe=False)