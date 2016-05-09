from django.shortcuts import redirect
from django.http.response import JsonResponse
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


def recipe_json(request):
    return JsonResponse([r.to_json() for r in models.Recipe.objects.all()], safe=False)


def meal_edit_eaten(request):
    if request.is_ajax():
        if request.POST:
            pk = request.POST.get('pk')
            value = int(request.POST.get('value'))
            try:
                model = models.DinnerPlanItem.objects.get(pk=pk)
                model.eaten = True if value == 1 else False
                model.save()
                return JsonResponse({'info': 'Object updated successfully'})
            except ObjectDoesNotExist as e:
                return JsonResponse({'error': 'Could not change object state'})
    return JsonResponse({'error': 'Something went wrong'})  # Wrong message