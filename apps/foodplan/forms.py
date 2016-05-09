from django import forms
from django.forms.models import inlineformset_factory
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
        exclude = ['end_date']
        widgets = {
            'start_date': forms.TextInput(attrs={
                'placeholder': 'yyyy-mm-dd',
                'class': 'mdl-textfield__input'
            }),
            'cost': forms.TextInput(attrs={
                'class': 'mdl-textfield__input'
            })
        }

ItemFormSet = inlineformset_factory(models.DinnerPlan, models.DinnerPlanItem, form=DinnerPlanForm, extra=0,
                                    can_delete=False,
                                    widgets={
                                        'recipe': forms.Select(attrs={'class': 'recipe-select2'}),
                                        'day': forms.Select(attrs={'class': 'day-select2'}),
                                        'eaten': forms.CheckboxInput(attrs={'class': 'mdl-checkbox__input'})
                                    })

