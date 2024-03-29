from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy
from django.http.response import JsonResponse, HttpResponse
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
    def __init__(self):
        self.kwargs = None

    def get_object(self):
        query = '%s-W%s' % (self.kwargs['year'], self.kwargs['week'])
        week_start = utils.get_start_date_from_year_and_week(query)
        model = models.DinnerPlan.objects.get(start_date=week_start)
        return model


class DinnerPlanIndex(LoginRequiredMixin, generic.DetailView):
    model = models.DinnerPlan
    template_name = 'foodplan/plan_details.html'
    context_object_name = 'plan'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object:
            messages.error(request, 'No plan for this week, please create one!')
            return redirect('food:plan_create')
        return super(DinnerPlanIndex, self).get(request, *args, **kwargs)

    def get_object(self):
        """
        Returns most recent plan if found, else None
        :return: Most recent DinnerPlan or None
        """
        plan = self.model.objects.current_plan()
        return plan

    def get_context_data(self, **kwargs):
        context = super(DinnerPlanIndex, self).get_context_data(**kwargs)
        # most_eaten = models.Recipe.objects.get(id=models.DinnerPlanItem.objects.values('recipe__id').annotate(num_recipes=Count('recipe_id')).latest('num_recipes')['recipe__id'])
        context['average_cost'] = self.object.cost / 7
        return context


class DinnerPlanDetails(LoginRequiredMixin, DinnerPlanObjectQueryMixin, generic.DetailView):
    template_name = 'foodplan/plan_details.html'
    context_object_name = 'plan'

    def get_context_data(self, **kwargs):
        context = super(DinnerPlanDetails, self).get_context_data(**kwargs)
        context['average_cost'] = self.object.cost / 7
        return context


class DinnerPlanCreate(LoginRequiredMixin, generic.CreateView):
    template_name = 'foodplan/plan_create.html'
    form_class = forms.DinnerPlanForm

    def get_context_data(self, **kwargs):
        context = super(DinnerPlanCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = forms.ItemFormSet(self.request.POST)
        else:
            context['formset'] = forms.ItemFormSet()
        return context

    def get_initial(self):
        return {
            'start_date': utils.get_today_as_string()
        }

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


class DinnerPlanUpdate(LoginRequiredMixin, DinnerPlanObjectQueryMixin, generic.UpdateView):
    template_name = 'foodplan/plan_create.html'
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


class DinnerPlanList(LoginRequiredMixin, generic.ListView):
    template_name = 'foodplan/plan_list.html'
    ordering = ['-start_date']
    model = models.DinnerPlan


class RecipesIndex(LoginRequiredMixin, generic.ListView):
    template_name = 'foodplan/recipe_list.html'
    paginate_by = 10
    context_object_name = 'recipes'
    queryset = models.Recipe.objects.all()


class RecipeCreate(LoginRequiredMixin, generic.CreateView):
    model = models.Recipe
    form_class = forms.RecipeForm
    template_name = 'foodplan/recipe_create.html'
    success_url = reverse_lazy('food:index')
    # TODO: Need to add view for single recipes to avoid NoReverseMatch when creating from /food/recipe/add/

    # def form_valid(self, form):
    #     super(RecipeCreate, self).form_valid(form)

    #
    #  def form_invalid(self, form):
    #     print('invalid')
    #     print(form)

class RecipeUpdate(LoginRequiredMixin, generic.UpdateView):
    form_class = forms.RecipeForm
    template_name = 'foodplan/recipe_create.html'
    context_object_name = 'recipe'


# TODO: Check for returning Unauthorized here instead of redirect
@login_required
def recipe_json(request):
    return JsonResponse([r.to_json() for r in models.Recipe.objects.all()], safe=False)


@login_required
def meal_edit_eaten(request):
    if request.is_ajax():
        if request.POST:
            pk = request.POST.get('pk')
            value = int(request.POST.get('value'))
            try:
                model = models.DinnerPlanItem.objects.get(pk=pk)
                model.eaten = True if value == 1 else False
                model.save()
            except models.DinnerPlanItem.DoesNotExist as e:
                return HttpResponse(status=412, content='Unknown DinnerPlanItem ID: %s' % pk)
            return HttpResponse(status=200)
    return HttpResponse(status=404)  # Wrong message
