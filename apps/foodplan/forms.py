from django import forms
from . import models


class DateInput(forms.DateInput):
    """
    Overrides default date input to ensure type="date"
    """
    input_type = 'date'


class DinnerPlanForm(forms.ModelForm):
    """
    Form for DinnerPlan Create/Update
    """

    class Meta:
        model = models.DinnerPlan
        fields = ['start_date', 'cost']


class CustomAddPlanItemForm(forms.ModelForm):
    class Meta:
        model = models.DinnerPlanItem
        fields = ['day', 'recipe']
