from django import forms
from . import models


class DateInput(forms.DateInput):
    """
    Overrides default date input to ensure type="date"
    """
    input_type = 'date'


class DinnerPlanForm(forms.ModelForm):

    class Meta:
        model = models.DinnerPlan
        fields = ['start_date', 'cost']
        widgets = {
            'meals': forms.CheckboxSelectMultiple()
        }


# family dinnerplan
# child = recipe

class DinnerPlanItemAddForm(forms.ModelForm):
    recipe = forms.ChoiceField(choices=[(r.id, r.title) for r in models.Recipe.objects.all()])
    start_date = forms.CharField(widget=forms.HiddenInput())
    day = forms.IntegerField(widget=forms.Select(choices=models.DinnerPlanItem.WEEKDAYS))

    class Meta:
        model = models.Recipe
        exclude = ['title', 'url', 'slug']
        fields = ('recipe',)
        widgets = {
            'recipe': forms.Select(attrs={'class': 'select'})
        }

    def save(self, commit=True):
        # recipe = super(DinnerPlanItemAddForm, self).save()  # Save the dinner plan item for id to m2m
        recipe = self.cleaned_data.get('recipe')
        start_date = self.cleaned_data.get('start_date')
        recipe = models.Recipe.objects.get(id=recipe)
        dinner_plan = models.DinnerPlan.objects.get(start_date=start_date.split(' ')[0])
        day = self.cleaned_data['day']
        models.DinnerPlanItem.objects.create(plan=dinner_plan, recipe=recipe, day=day)

        return recipe


class DinnerPlanItemEditForm(forms.ModelForm):

    class Meta:
        model = models.DinnerPlanItem
        exclude = []
